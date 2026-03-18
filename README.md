# Japan Real Estate API

Japan real estate and housing market data including urbanization rates, construction activity, household spending, credit availability, interest rates, and foreign investment. Powered by World Bank Open Data.

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All housing market indicators snapshot |
| `GET /urban-population` | Urban population (% of total) |
| `GET /urban-growth` | Urban population growth rate |
| `GET /construction` | Manufacturing & construction value added |
| `GET /household-spending` | Household consumption per capita |
| `GET /credit` | Domestic credit to private sector |
| `GET /interest-rate` | Real interest rate |
| `GET /lending-rate` | Lending interest rate |
| `GET /fdi` | Foreign direct investment inflows |

## Data Source

World Bank Open Data
https://data.worldbank.org/country/JP

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
