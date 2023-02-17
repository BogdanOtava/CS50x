/*
https://cs50.harvard.edu/x/2023/psets/7/fiftyville/
*/

-- We know the theft took place on Humphrey St., on July 28 2021.

SELECT *
FROM crime_scene_reports
WHERE street = "Humphrey Street" AND year = 2021 AND month = 7 AND day = 28;

-- By checking the crime scene reports we found out that it took place at 10:15 AM at the bakery.
-- Three witnesses were present each mentioning the bakery.

SELECT *
FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28;

-- By checking the interviews that took place on that day, we found out after 10 minutes of the theft,
-- the thief got into a car in the bakery parking lot and drove away.
-- Also someone mentioned that he recognized the thief because earlier that morning he saw the thief withdrawing some money on Leggett Street.
-- The thief called someone after leaving the bakery and talked to them for less than a minute.
-- The thief said on the phone that they were planning to take the earliest flight out of Fiftyville tomorrow and asked the person he was talking to to buy the tickets.

SELECT *
FROM people
WHERE license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE activity = "exit" AND year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 40
)
AND phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
)
AND people.id IN (
    SELECT person_id
    FROM bank_accounts
    WHERE bank_accounts.account_number IN (
        SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"
    )
);

-- Following the leads about the bakery parking and the ATM withdrawal and the call, we get back 3 suspects.
-- Taylor, Diana and Bruce.

SELECT *
FROM people
WHERE phone_number IN (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60 AND caller IN ("(286) 555-6063", "(770) 555-1861", "(367) 555-5533")
);

-- If we check the receivers of those phone calls against the 3 suspects phone numbers, we get 3 names that might be the accomplices.
-- James, Philip and Robin.

SELECT *
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
AND caller IN ("(286) 555-6063", "(770) 555-1861", "(367) 555-5533")
AND receiver IN ("(676) 555-6554", "(725) 555-3243", "(375) 555-8161");

-- Knowing the names of the possible suspects and accomplices we can check who called who.
-- Taylor called James, Diana called Philip and Bruce called Robin.

SELECT *
FROM flights
JOIN airports
ON airports.id = flights.origin_airport_id
WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.hour BETWEEN 00 AND 12 AND airports.city = "Fiftyville"
ORDER BY flights.hour, flights.minute;

SELECT full_name, city
FROM airports
WHERE id IN (1, 4, 11);

-- The thief said he wants to leave as early as possible tomorrow.
-- Checking the earliest flights we get back 3 flights: to New York at 8:20 AM, to Chicago at 9:30 AM and to San Francisco at 12:15 PM.

SELECT name, passport_number
FROM people
WHERE people.name IN ("Bruce", "Taylor", "Diana", "James", "Philip", "Robin")
AND passport_number IN (
    SELECT passport_number
    FROM passengers
    JOIN flights
    ON flights.id = passengers.flight_id
    JOIN airports
    ON airports.id = flights.origin_airport_id
    WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND flights.hour BETWEEN 00 AND 12
    AND flights.origin_airport_id IN (
        SELECT airports.id
        FROM airports
        WHERE airports.city = "Fiftyville"
    )
    AND flights.destination_airport_id IN (
        SELECT airports.id
        FROM airports
        WHERE airports.city IN ("New York City", "Chicago", "San Francisco")
    )
);

-- From the three suspects, Bruce and Taylor flew on the 29th on one of the three aforementioned flights.

SELECT full_name, city, passport_number, flights.destination_airport_id, flights.hour, flights.minute
FROM airports
JOIN flights
ON flights.origin_airport_id = airports.id
JOIN passengers
ON passengers.flight_id = flights.id
WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29 AND hour BETWEEN 00 AND 12
AND passengers.passport_number IN (
    SELECT passport_number
    FROM people
    WHERE people.name IN ("Bruce", "Taylor", "Diana", "James", "Philip", "Robin")
);

-- Both of them flew to New York without the accomplices.

-- From the information gathered so far there are two options:
-- Thief: Taylor | Accomplice: James | Flew to: New York.
-- Thief: Bruce  | Accomplice: Robin | Flew to: New York.
