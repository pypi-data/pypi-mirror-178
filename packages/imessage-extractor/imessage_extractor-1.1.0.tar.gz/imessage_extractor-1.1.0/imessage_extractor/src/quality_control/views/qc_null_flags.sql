drop view if exists qc_null_flags;
create view qc_null_flags as

select *
from message_user
where is_from_me is null
   or is_text is null
   or is_text_parsed_from_attributedbody is null
   or is_url is null
   or is_group_chat is null
   or is_emote is null
   or has_no_text is null
   or has_attachment is null
   or is_attachment is null
   or has_attachment_image is null
   or is_attachment_image is null
   or is_thread_reply is null
   or is_thread_origin is null
   or is_edited is null
   or was_unsent is null
order by message_id desc
