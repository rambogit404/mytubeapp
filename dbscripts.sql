-- CREATE SCHEMA `mytubedb` ; 

-- CREATE TABLE mytube_data (
-- channel_id varchar(50) DEFAULT NULL,
--   video_id varchar(50) DEFAULT NULL,
--   tile_of_video varchar(200) DEFAULT NULL,
--   youtube_video_link varchar(2050) DEFAULT NULL,
--   s3_download_link varchar(2050) DEFAULT NULL,
--   youtube_thumbnail_url varchar(2050) DEFAULT NULL,
--   likes_count integer DEFAULT NULL,
--   comments_count integer DEFAULT NULL
-- );


select * from mytube_data;

insert into mytube_data values ("devtest", "devtest", "rama gaadi prj", "ytlink", "s3link", "ytd thumb", "23010", "393884");

commit;

truncate mytube_data;