## Setting proxy country
You can use the `proxy_country` parameter to set a proxy country. The default is `UnitedStates`, and it's recommended to change it since your page could not be available from all locations.

To scrape the page from the United States you have to set `proxy_country` to `UnitedStates`:
```bash
curl https://api.parsera.org/v1/extract \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR-API-KEY>' \
--data '{
    "url": <TARGET-URL>,
    "attributes": [
        {
            "name": <First attribute name>,
            "description": <First attribute description>,
        },
        {
            "name": <Second attribute name>,
            "description": <Second attribute description>
        }
    ],
    "proxy_country": "UnitedStates"
}'

```

## List of proxy countries

Send a `GET` request to this URL [https://api.parsera.org/v1/proxy-countries](https://api.parsera.org/v1/proxy-countries), to get the list of countries programmatically.

Here is the list of countries available:

- Random Country - `random`
- Afghanistan - `Afghanistan`
- Albania - `Albania`
- Algeria - `Algeria`
- Argentina - `Argentina`
- Armenia - `Armenia`
- Aruba - `Aruba`
- Australia - `Australia`
- Austria - `Austria`
- Azerbaijan - `Azerbaijan`
- Bahamas - `Bahamas`
- Bahrain - `Bahrain`
- Bangladesh - `Bangladesh`
- Belarus - `Belarus`
- Belgium - `Belgium`
- Bosnia and Herzegovina - `BosniaandHerzegovina`
- Brazil - `Brazil`
- British Virgin Islands - `BritishVirginIslands`
- Brunei - `Brunei`
- Bulgaria - `Bulgaria`
- Cambodia - `Cambodia`
- Cameroon - `Cameroon`
- Canada - `Canada`
- Chile - `Chile`
- China - `China`
- Colombia - `Colombia`
- Costa Rica - `CostaRica`
- Croatia - `Croatia`
- Cuba - `Cuba`
- Cyprus - `Cyprus`
- Chechia - `Chechia`
- Denmark - `Denmark`
- Dominican Republic - `DominicanRepublic`
- Ecuador - `Ecuador`
- Egypt - `Egypt`
- El Salvador - `ElSalvador`
- Estonia - `Estonia`
- Ethiopia - `Ethiopia`
- Finland - `Finland`
- France - `France`
- Georgia - `Georgia`
- Germany - `Germany`
- Ghana - `Ghana`
- Greece - `Greece`
- Guatemala - `Guatemala`
- Guyana - `Guyana`
- Hashemite Kingdom of Jordan - `HashemiteKingdomofJordan`
- Hong Kong - `HongKong`
- Hungary - `Hungary`
- India - `India`
- Indonesia - `Indonesia`
- Iraq - `Iraq`
- Ireland - `Ireland`
- Israel - `Israel`
- Italy - `Italy`
- Jamaica - `Jamaica`
- Japan - `Japan`
- Kazakhstan - `Kazakhstan`
- Kenya - `Kenya`
- Kuwait - `Kuwait`
- Latvia - `Latvia`
- Liechtenstein - `Liechtenstein`
- Luxembourg - `Luxembourg`
- Macedonia - `Macedonia`
- Madagascar - `Madagascar`
- Malaysia - `Malaysia`
- Mauritius - `Mauritius`
- Mexico - `Mexico`
- Mongolia - `Mongolia`
- Montenegro - `Montenegro`
- Morocco - `Morocco`
- Mozambique - `Mozambique`
- Myanmar - `Myanmar`
- Nepal - `Nepal`
- Netherlands - `Netherlands`
- New Zealand - `NewZealand`
- Nigeria - `Nigeria`
- Norway - `Norway`
- Oman - `Oman`
- Pakistan - `Pakistan`
- Panama - `Panama`
- Papua New Guinea - `PapuaNewGuinea`
- Paraguay - `Paraguay`
- Peru - `Peru`
- Philippines - `Philippines`
- Poland - `Poland`
- Portugal - `Portugal`
- Puerto Rico - `PuertoRico`
- Qatar - `Qatar`
- Republic of Lithuania - `RepublicOfLithuania`
- Republic of Moldova - `RepublicOfMoldova`
- Romania - `Romania`
- Russia - `Russia`
- Saudi Arabia - `SaudiArabia`
- Senegal - `Senegal`
- Serbia - `Serbia`
- Seychelles - `Seychelles`
- Singapore - `Singapore`
- Slovakia - `Slovakia`
- Slovenia - `Slovenia`
- Somalia - `Somalia`
- South Africa - `SouthAfrica`
- South Korea - `SouthKorea`
- Spain - `Spain`
- Sri Lanka - `SriLanka`
- Sudan - `Sudan`
- Suriname - `Suriname`
- Sweden - `Sweden`
- Switzerland - `Switzerland`
- Syria - `Syria`
- Taiwan - `Taiwan`
- Tajikistan - `Tajikistan`
- Thailand - `Thailand`
- Trinidad and Tobago - `TrinidadandTobago`
- Tunisia - `Tunisia`
- Turkey - `Turkey`
- Uganda - `Uganda`
- Ukraine - `Ukraine`
- United Arab Emirates - `UnitedArabEmirates`
- United Kingdom - `UnitedKingdom`
- United States - `UnitedStates`
- Uzbekistan - `Uzbekistan`
- Venezuela - `Venezuela`
- Vietnam - `Vietnam`
- Zambia - `Zambia`