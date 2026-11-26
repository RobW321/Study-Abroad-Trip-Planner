
-- =========================================================
-- Study Abroad Trip Planner
-- SQL Server database initialization
-- =========================================================
-- Passwords are supplied through SQLCMD variables.
-- This script is safe to execute multiple times.

-- 1. Create the Trips database if it does not exist.
IF DB_ID('TripsDB') IS NULL
BEGIN
    CREATE DATABASE TripsDB;
END;
GO

-- 2. Create the Expenses database if it does not exist.
IF DB_ID('ExpensesDB') IS NULL
BEGIN
    CREATE DATABASE ExpensesDB;
END;
GO

-- 3. Create the Trips service login if it does not exist.
IF NOT EXISTS (
    SELECT 1
    FROM sys.sql_logins
    WHERE name = 'trips_user'
)
BEGIN
    CREATE LOGIN trips_user
    WITH PASSWORD = '$(TRIPS_DB_PASSWORD)',
         CHECK_POLICY = OFF;
END;
GO

-- 4. Create the Expenses service login if it does not exist.
IF NOT EXISTS (
    SELECT 1
    FROM sys.sql_logins
    WHERE name = 'expenses_user'
)
BEGIN
    CREATE LOGIN expenses_user
    WITH PASSWORD = '$(EXPENSES_DB_PASSWORD)',
         CHECK_POLICY = OFF;
END;
GO

-- 5. Configure the Trips database user and permissions.
USE TripsDB;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE name = 'trips_user'
)
BEGIN
    CREATE USER trips_user FOR LOGIN trips_user;
END;
GO

IF IS_ROLEMEMBER('db_owner', 'trips_user') <> 1
BEGIN
    ALTER ROLE db_owner ADD MEMBER trips_user;
END;
GO

-- 6. Configure the Expenses database user and permissions.
USE ExpensesDB;
GO

IF NOT EXISTS (
    SELECT 1
    FROM sys.database_principals
    WHERE name = 'expenses_user'
)
BEGIN
    CREATE USER expenses_user FOR LOGIN expenses_user;
END;
GO

IF IS_ROLEMEMBER('db_owner', 'expenses_user') <> 1
BEGIN
    ALTER ROLE db_owner ADD MEMBER expenses_user;
END;
GO
