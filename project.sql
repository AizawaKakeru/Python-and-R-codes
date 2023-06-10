Select TOP 1 p.profile_id, p.full_name, p.phone from Profiles p
INNER JOIN Tenancy_history ON Tenancy_history.profile_id = p.profile_id
ORDER BY STAY DESC

Select p.full_name, p.email, p.phone from Profiles p
INNER JOIN Tenancy_history ON Tenancy_history.profile_id = p.profile_id
WHERE Tenancy_history.rent > 9000
AND p.marital_status = 'Y'


SELECT p.profile_id, p.full_name,p.phone,p.email, p.city, Tenancy_history.house_id,Tenancy_history.move_in_date,Tenancy_history.move_out_date,
Tenancy_history.rent,Referrals.referral_valid,Employment_details.latest_employer,Employment_details.Occupational_category
FROM Profiles p
INNER JOIN Tenancy_history ON Tenancy_history.profile_id = p.profile_id
INNER JOIN Referrals ON Referrals.referrer_id = p.profile_id
INNER JOIN Employment_details ON Employment_details.profile_id = p.profile_id
WHERE p.city='BANGALORE' OR p.city = 'PUNE'
AND Tenancy_history.move_in_date > '2015-01-01' AND Tenancy_history.move_out_date < '2016-01-01'
ORDER BY Tenancy_history.rent DESC


Select p.full_name, p.email, p.phone, p.referral_code,Referrals.referrer_bonus_amount*Referrals.referral_valid as BONUS
FROM Profiles p
INNER JOIN Referrals ON Referrals.referrer_id = p.profile_id
WHERE Referrals.referral_valid = 1
OR Referrals.referral_valid > 1

Select SUM(Tenancy_history.rent) as RENT_BY_PRICE,Profiles.city from Tenancy_history
INNER JOIN Profiles ON Tenancy_history.profile_id = Profiles.profile_id
GROUP BY Profiles.city
Select SUM(Tenancy_history.rent) as TOTAL_RENT from Tenancy_history
INNER JOIN Profiles ON Tenancy_history.profile_id = Profiles.profile_id


CREATE VIEW
vw_tenant
AS 
Select th.profile_id, th.move_in_date, th.rent,Houses.Beds_vacant, Houses.house_type, Addresses.description,Addresses.city from Tenancy_history th
INNER JOIN Houses ON th.house_id = Houses.house_id
INNER JOIN Addresses ON th.house_id = Addresses.house_id
WHERE th.move_in_date = '2015-04-30' OR th.move_in_date > '2015-04-30'
AND Houses.Beds_vacant > 0


Select DATEADD(MONTH,1,valid_till) AS NEW_DATE from Referrals
WHERE Referrals.referral_valid >2


UPDATE Profiles
SET CUSTOMER_SEGMENT = 'GRADE C'
WHERE RENT =7500 OR RENT < 7500
UPDATE Profiles
SET CUSTOMER_SEGMENT = 'GRADE B'
WHERE RENT > 7500 AND RENT < 10000
UPDATE Profiles
SET CUSTOMER_SEGMENT = 'GRADE A'
WHERE RENT > 10000 OR RENT =10000


Select p.full_name, p.phone, p.city,Houses.house_type, Houses.furnishing_type, Addresses.description FROM Profiles p
INNER JOIN Tenancy_history ON p.profile_id = Tenancy_history.profile_id
INNER JOIN Houses ON Houses.house_id = Tenancy_history.house_id
INNER JOIN Addresses on Addresses.house_id = Houses.house_id
INNER JOIN Referrals on Referrals.referrer_id = p.profile_id
WHERE Referrals.referral_valid = 0


Select TOP 1 Addresses.name, Addresses.description, Addresses.pincode, Addresses.pincode, Addresses.city, Houses.house_type, Houses.furnishing_type, Houses.bhk_details FROM Houses
INNER JOIN Addresses on Addresses.house_id = Houses.house_id
ORDER BY Houses.Beds_vacant ASC
