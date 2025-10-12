-- GOOGLE SHEET DATA SAYFASININ AKTARILMASI
INSERT INTO MAIN_DATA
 (ID, TYPE, TITLE_TYPE, IMDB_TT, ORIGINAL_TITLE, PRIMARY_TITLE, RELEASE_YEAR, STATUS, SCORE, SCORE_DATE, DURATION, RATING, RATING_COUNT, GENRES, WATCH_GRADE, INSERT_DATE, MANUAL_UPDATE_DATE, AUTOMATIC_UPDATE_DATE)
SELECT ID
		,Type
		,TitleType
		,IMDbTT
		,OriginalTitle
		,PrimaryTitle
		,ReleaseYear
		,Status
		,Score
		--,ScoreDate
		,CASE WHEN ScoreDate IS NULL THEN "1900-01-01" ELSE substr(ScoreDate,7,4) || '-' || substr(ScoreDate,4,2) || '-' || substr(ScoreDate,1,2) END AS SCORE_DATE_NEW
		,Duration
		--,Rating
		,CASE WHEN Rating = 'Rating not available' THEN NULL ELSE replace(Rating, ',', '.') END AS RATING_NEW
		--,RatingCount
		,CASE WHEN RatingCount = 'Rating count not available' THEN NULL ELSE RatingCount END AS RATING_COUNT_NEW
		,Genres
		,WatchGrade
		--,InsertDate
		,CASE WHEN InsertDate IS NULL THEN "1900-01-01" ELSE substr(InsertDate,7,4) || '-' || substr(InsertDate,4,2) || '-' || substr(InsertDate,1,2) END AS INSERT_DATE_NEW
		--,ManualUpdateDate
		,CASE WHEN ManualUpdateDate IS NULL THEN "1900-01-01" ELSE substr(ManualUpdateDate,7,4) || '-' || substr(ManualUpdateDate,4,2) || '-' || substr(ManualUpdateDate,1,2) END AS MANUAL_UPDATE_DATE_NEW
		--,AutomaticUpdateDate
		,CASE WHEN AutomaticUpdateDate IS NULL THEN "1900-01-01" ELSE substr(AutomaticUpdateDate,7,4) || '-' || substr(AutomaticUpdateDate,4,2) || '-' || substr(AutomaticUpdateDate,1,2) END AS AUTOMATIC_UPDATE_DATE_NEW
FROM GOOGLE_SHEETS_MAIN_DATA
--LIMIT 500




-- 20250606 SORGUSU
-- GOOGLE SHEET DATA SAYFASININ AKTARILMASI
INSERT INTO MAIN_DATA
 (ID, TYPE, TITLE_TYPE, IMDB_TT, ORIGINAL_TITLE, PRIMARY_TITLE, RELEASE_YEAR, STATUS, SCORE, SCORE_DATE, DURATION, RATING, RATING_COUNT, GENRES, WATCH_GRADE, INSERT_DATE, MANUAL_UPDATE_DATE, AUTOMATIC_UPDATE_DATE)
 SELECT ID
		,Type
		,[Title Type]
		,[IMDb TT]
		,[Original Title]
		,[Primary Title]
		,[Release Year]
		,Status
		,Score
		--,ScoreDate
		,CASE WHEN [Score Date] IS NULL THEN "1900-01-01" ELSE substr([Score Date],7,4) || '-' || substr([Score Date],4,2) || '-' || substr([Score Date],1,2) END AS SCORE_DATE_NEW

		,Duration
		--,Rating
		,CASE WHEN Rating = 'Rating not available' THEN NULL ELSE replace(Rating, ',', '.') END AS RATING_NEW

		--,RatingCount
		,CASE WHEN [Rating Count] = 'Rating count not available' THEN NULL ELSE [Rating Count] END AS RATING_COUNT_NEW
		
		,Genres
		,[Watch Grade]
		--,InsertDate
		,CASE WHEN [Insert Date] IS NULL THEN "1900-01-01" ELSE substr([Insert Date],7,4) || '-' || substr([Insert Date],4,2) || '-' || substr([Insert Date],1,2) END AS INSERT_DATE_NEW
		--,ManualUpdateDate
		,CASE WHEN [Manual Update Date] IS NULL THEN "1900-01-01" ELSE substr([Manual Update Date],7,4) || '-' || substr([Manual Update Date],4,2) || '-' || substr([Manual Update Date],1,2) END AS MANUAL_UPDATE_DATE_NEW
		--,AutomaticUpdateDate
		,CASE WHEN [Automatic Update Date] IS NULL THEN "1900-01-01" ELSE substr([Automatic Update Date],7,4) || '-' || substr([Automatic Update Date],4,2) || '-' || substr([Automatic Update Date],1,2) END AS AUTOMATIC_UPDATE_DATE_NEW
FROM GOOGLE_SHEETS_MAIN_DATA
