USE `world`;

DROP PROCEDURE IF EXISTS DataPreprocessing;

DELIMITER $$
CREATE PROCEDURE DataPreprocessing()
    BEGIN
        WITH city_highest_population AS (
            SELECT 
                CountryCode, 
                Name, 
                District,
                Population
            FROM 
                (
                    SELECT 
                        CountryCode, 
                        Name, 
                        District,
                        Population,
                        RANK() OVER (PARTITION BY CountryCode ORDER BY Population DESC) as Order_city_size
                    FROM city
                ) c 
            WHERE Order_city_size = 1   
        )
        , Country_official_language AS (
            SELECT 
                CountryCode,
                Language,
                Percentage
            FROM countrylanguage
            WHERE IsOfficial = 'T'
        )
        SELECT 
            cty.Code, 
            cty.Name,
            -- LocalName,
            cty.Continent, 
            cty.Region,
            cty.SurfaceArea,
            cty.IndepYear,
            cty.Population,
            cty.LifeExpectancy,
            -- GNPOld,
            cty.GovernmentForm,
            -- HeadOfState,
            -- Capital,
            -- Code2,
            chp.Name as CityName_highest_population,
            chp.District as CityDistrict_highest_population,
            chp.Population as CityPopulation_highest,
            col.Language as OfficialLanguage,
            col.Percentage as OfficialLanguage_percentage,
            cty.GNP
        FROM country cty
        LEFT JOIN city_highest_population chp
        ON chp.CountryCode = cty.Code
        LEFT JOIN Country_official_language col
        ON col.CountryCode = cty.Code
        ;

    END $$
DELIMITER ;
