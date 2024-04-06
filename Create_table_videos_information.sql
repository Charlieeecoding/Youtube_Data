-- Step 1: Drop table, in case of any duplicated table name
DROP TABLE YOUTUBE_API.DBO.VIDEOS_INFORMATION
;

-- Step 2: Create a new table
CREATE TABLE YOUTUBE_API.DBO.VIDEOS_INFORMATION (
  VIDEO_ID VARCHAR(MAX),
  TITLE VARCHAR(MAX),
  PUBLISH_DATE VARCHAR(MAX), 
  DESCRIPTION VARCHAR(MAX),
)
;

-- Step 3: Read data from the CSV file and insert into the table
BULK INSERT YOUTUBE_API.DBO.VIDEOS_INFORMATION
FROM 'C:\Users\Charlie Yung\Desktop\Project\Youtube_API\ForSQLDatabase\videos_information.csv'
WITH (
  FIRSTROW = 2, -- Skip the header row if present
  FIELDTERMINATOR = ',', -- Specify the field delimiter
  ROWTERMINATOR = '\n' -- Specify the row delimiter
)
;

-- Step 4: Check the table result
SELECT *
FROM YOUTUBE_API.DBO.VIDEOS_INFORMATION
;