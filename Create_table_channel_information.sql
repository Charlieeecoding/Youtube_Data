-- Step 1: Drop table, in case of any duplicated table name
DROP TABLE YOUTUBE_API.DBO.CHANNEL_INFORMATION 
;

-- Step 2: Create a new table
CREATE TABLE YOUTUBE_API.DBO.CHANNEL_INFORMATION (
  CHANNEL_NAME VARCHAR(MAX),
  CHANNEL_ID VARCHAR(MAX),
  PUBLISH_AT VARCHAR(MAX), 
  SUBSCRIBER_COUNT INT,
  VIDEO_COUNT INT, 
  DESCRIPTION VARCHAR(MAX), 
  LOG_TIME VARCHAR(MAX)
)
;

-- Step 3: Read data from the CSV file and insert into the table
BULK INSERT YOUTUBE_API.DBO.CHANNEL_INFORMATION
FROM 'C:\Users\Charlie Yung\Desktop\Project\Youtube_API\ForSQLDatabase\channel_information.csv'
WITH (
  FIRSTROW = 2, -- Skip the header row if present
  FIELDTERMINATOR = ',', -- Specify the field delimiter
  ROWTERMINATOR = '\n' -- Specify the row delimiter
)
;

-- Step 4: Check the table result
SELECT * 
FROM YOUTUBE_API.DBO.CHANNEL_INFORMATION
;
