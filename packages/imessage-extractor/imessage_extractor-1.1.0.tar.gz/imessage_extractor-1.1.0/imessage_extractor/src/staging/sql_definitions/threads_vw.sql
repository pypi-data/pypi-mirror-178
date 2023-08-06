drop view if exists threads_vw;
create view threads_vw as

select message_id
       , coalesce(thread_original_message_id, message_id) as thread_original_message_id
       , is_thread_reply
       , is_thread_origin
from message_user
where thread_original_message_id is not null
  or is_thread_origin = 1
order by thread_original_message_id desc, ts desc
