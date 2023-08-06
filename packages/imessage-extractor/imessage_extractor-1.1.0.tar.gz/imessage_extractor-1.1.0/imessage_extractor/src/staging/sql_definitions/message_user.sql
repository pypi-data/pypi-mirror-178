drop table if exists message_user;
create table message_user as

-- Gather information about the types of messages sent and received
with message_types as (
    select ROWID
           , service
           , case when associated_message_type in (2000, 2001, 2002, 2003, 2004, 2005, 3000, 3001, 3002, 3003, 3004, 3005) then true
                  else false
             end as is_emote
           , case when "text" like 'http:%' or "text" like 'https:%' then true else false
             end as is_url
           , associated_message_type
           , case when balloon_bundle_id like '%PeerPaymentMessagesExtension' then 'apple_cash'
                  when associated_message_type = 2 and balloon_bundle_id like '%imessagepoll%' then 'poll'
                  when associated_message_type in (2, 3) and balloon_bundle_id like '%gamepigeon%' then 'game_pigeon'
                  when associated_message_type in (2, 3) and balloon_bundle_id like '%messages.business.extension%' then 'business_extension'
                  when associated_message_type = 3 and "text" like '%earned an achievement.' then 'activity'
                  when associated_message_type = 3 and "text" like '%completed a workout.' then 'activity'
                  when associated_message_type = 3 and "text" like '%closed all three Activity rings.' then 'activity'
                  when associated_message_type = 3 and "text" like 'Requested % with Apple Pay.' then 'apple_cash'
                  when associated_message_type = 3 and ("text" like '%poll%' or "text" like '%voted%') then 'poll'
                  when associated_message_type = 3 and "text" = 'Cup Pong' then 'game_pigeon'
                  when associated_message_type = 3 and "text" = '8 Ball' then 'game_pigeon'
                  when associated_message_type = 3 and "text" = '(null)' then 'null_message'
                  when associated_message_type = 1000 and cache_has_attachments = true and was_data_detected = true then 'sticker'
                  when associated_message_type = 2000 then 'emote_love'
                  when associated_message_type = 2001 then 'emote_like'
                  when associated_message_type = 2002 then 'emote_dislike'
                  when associated_message_type = 2003 then 'emote_laugh'
                  when associated_message_type = 2004 then 'emote_emphasis'
                  when associated_message_type = 2005 then 'emote_question'
                  when associated_message_type = 3000 then 'emote_remove_heart'
                  when associated_message_type = 3001 then 'emote_remove_like'
                  when associated_message_type = 3002 then 'emote_remove_dislike'
                  when associated_message_type = 3003 then 'emote_remove_laugh'
                  when associated_message_type = 3004 then 'emote_remove_emphasis'
                  when associated_message_type = 3005 then 'emote_remove_question'
                  else null
               end as message_special_type
           , case when is_read = 1
                  and part_count = 0
                  and date_edited > 0
                  and attributedBody is null
                  then true
                  else false
             end as was_unsent
    from message
)

-- Cleanly extract message text
, message_text as (
    select ROWID
           , case when "text" = '' then null
                  when "text" = '�' then null
                  when is_emote = true then null
                  when is_url = true then null
                  else "text"
            end as "text"
          --  , "text"
           , is_text_parsed_from_attributedbody
    from (
        select t1.ROWID
               -- char(13) = carriage return, char(10) = line break
               , trim(replace(replace(replace(t1."text", '￼', ''), char(13), ' '), char(10), ' ')) as "text"
               , t1.is_text_parsed_from_attributedbody
               , mt.is_emote
               , mt.is_url
        from (
            select m.ROWID
	    		   , coalesce(m."text", a."text") as "text"
	    		   , coalesce(a.is_text_parsed_from_attributedbody, 0) as is_text_parsed_from_attributedbody
			from message m
			left join message_text_parsed_from_attributedbody a
			  on m.ROWID = a.message_id
		) t1
        join message_types mt
          on t1.ROWID = mt.ROWID
    ) t2
)

-- Finalize information about the types of messages sent and received
, message_types2 as (
    select mt.ROWID
           , service
           , mt.associated_message_type
           , mt.message_special_type
           , mt.is_emote
           , mt.is_url
           , case when mt.is_emote = false
                  and mt.is_url = false
                  and mt.message_special_type is null
                  and tt.text is not null
                  then true
                  else false
             end as is_text
           , case when tt."text" is null then true else false end as has_no_text
           , mt.was_unsent
    from message_types mt
    join message_text tt
      on mt.ROWID = tt.ROWID
)

-- Attachment information by message
, attachments as (
    select m.ROWID
           , case when m.cache_has_attachments = true and mt.is_emote = false then true else false end as has_attachment
           , case when m.cache_has_attachments = true and mt.is_url = false and mt.is_text = false then true else false end as is_attachment
           , case when m.cache_has_attachments = true and mt.is_url = false and mt.message_special_type is null then true else false end as has_attachment_image
           , case when m.cache_has_attachments = true and mt.is_url = false and mt.message_special_type is null and mt.is_text = false then true else false end as is_attachment_image
    from message m
    join message_types2 mt
      on m.ROWID = mt.ROWID
)

-- Get the ROWID for all messages that have a thread_originator_guid and flags to
-- indicate whether the given message is the originator of a thread of a reply to
-- an existing thread
, threads as (
    select m1.ROWID
          , m2.ROWID as thread_original_message_id
          , case when m2.ROWID is not null then true else false end is_thread_reply
          , coalesce(thread_origins.is_thread_origin, false) as is_thread_origin
    from message m1
    left join message m2
      on m1.thread_originator_guid = m2.guid
    left join (
        select distinct m1.ROWID as message_id, true as is_thread_origin
        from message m1
        join message m2
          on m1.guid = m2.thread_originator_guid
    ) thread_origins
      on m1.ROWID = thread_origins.message_id
)

-- Which contacts and group chat(s) (if any) each message is associated with
, contacts_and_group_chat_info as (
    select m.ROWID
           , c.chat_identifier
           , n.contact_name
           , case when c.chat_identifier like 'chat%' then true else false end as is_group_chat
    from chat c
    join (select chat_id, message_id
          from (-- Use a window function to avoid one-to-many message_id: chat_id mappings
                select chat_id
                       , message_id
                       , row_number() over(partition by message_id order by message_date desc) as r
                from chat_message_join
          ) cm_join
          where r = 1
    ) cm_mapping
      on c.ROWID = cm_mapping.chat_id
    join message m
      on cm_mapping.message_id = m.ROWID
    left join contacts_user n
      on c.chat_identifier = n.chat_identifier
)

-- Message dates and times
, dates_and_times as (
    select sent_times.ROWID
           , sent_times.ts
           , sent_times.dt
           , read_by_them_times.ts_read_by_them
           , read_by_them_times.dt_read_by_them
           , read_by_them_times.elapsed_seconds_until_read
    from (
        select ROWID
               , ts
               , date(ts) as dt
        from (
            select ROWID
                   , datetime(`date` / 1000000000 + 978307200, 'unixepoch', 'localtime') as ts
            from message
        ) t1
    ) sent_times
    left join (
        select ROWID
               , ts_read_by_them
               , date(ts_read_by_them) as dt_read_by_them
               , cast(round((julianday(ts_read_by_them) - julianday(ts)) * 86400) as integer) as elapsed_seconds_until_read
        from (
            select m.ROWID
                   , datetime(m.`date` / 1000000000 + 978307200, 'unixepoch', 'localtime') as ts
                   , case when m.date_read != 0 then datetime(m.date_read / 1000000000 + 978307200, 'unixepoch', 'localtime') else null end as ts_read_by_them
            from message m
            join message_types2 mt
              on m.ROWID = mt.ROWID
            where m.is_from_me = true
              and mt.is_text = true
        ) r1
        where r1.ts_read_by_them > r1.ts
    ) read_by_them_times
      on sent_times.ROWID = read_by_them_times.ROWID
)

-- Edit info (as of macOS Ventura)
, edit_info as (
    select message_id, edit_history
    from message_text_edit_history_json
)


select cast(message.ROWID as integer) as message_id
       , cast(dates_and_times.ts as text) as ts
       , cast(dates_and_times.dt as text) as dt
       , cast(dates_and_times.ts_read_by_them as text) as ts_read_by_them
       , cast(dates_and_times.dt_read_by_them as text) as dt_read_by_them
       , cast(dates_and_times.elapsed_seconds_until_read as integer) as elapsed_seconds_until_read
       , cast(contacts_and_group_chat_info.chat_identifier as text) as chat_identifier
       , cast(contacts_and_group_chat_info.contact_name as text) as contact_name
       , cast(coalesce(contacts_and_group_chat_info.is_group_chat, false) as integer) as is_group_chat
       , cast(message_text."text" as text) as "text"
       , cast(message_text.is_text_parsed_from_attributedbody as integer) as is_text_parsed_from_attributedbody
       , cast(message.is_from_me as integer) as is_from_me
       , cast(message_types2.service as text) as service
       , cast(message_types2.message_special_type as text) as message_special_type
       , cast(message_types2.associated_message_type as text) as associated_message_type
       , cast(message_types2.is_emote as integer) as is_emote
       , cast(message_types2.is_url as integer) as is_url
       , cast(message_types2.is_text as integer) as is_text
       , cast(message_types2.has_no_text as integer) as has_no_text
       , cast(attachments.has_attachment as integer) as has_attachment
       , cast(attachments.is_attachment as integer) as is_attachment
       , cast(attachments.has_attachment_image as integer) as has_attachment_image
       , cast(attachments.is_attachment_image as integer) as is_attachment_image
       , cast(threads.thread_original_message_id as integer) as thread_original_message_id
       , cast(threads.is_thread_reply as integer) as is_thread_reply
       , cast(threads.is_thread_origin as integer) as is_thread_origin
       , cast(edit_info.edit_history as text) as edit_history
       , case when edit_info.edit_history is null then false else true end as is_edited
       , cast(message_types2.was_unsent as integer) as was_unsent
from message
left join message_types2
  on message.ROWID = message_types2.ROWID
left join message_text
  on message.ROWID = message_text.ROWID
left join attachments
  on message.ROWID = attachments.ROWID
left join threads
  on message.ROWID = threads.ROWID
left join contacts_and_group_chat_info
  on message.ROWID = contacts_and_group_chat_info.ROWID
left join dates_and_times
  on message.ROWID = dates_and_times.ROWID
left join edit_info
  on message.ROWID = edit_info.message_id
order by message.ROWID desc nulls last
