# Fields Reference

This page lists the available fields for each method family.

## App Methods (65+ fields)

### Basic Information

- `appId` – Package name (for example, `com.whatsapp`)
- `title` – App name
- `summary` – Short description
- `description` – Full description
- `url` – Google Play URL

### Ratings & Reviews

- `score` – Average rating (1–5)
- `ratings` – Total number of ratings
- `reviews` – Total number of reviews
- `histogram` – Rating distribution `[1★, 2★, 3★, 4★, 5★]`

### Install Metrics

- `installs` – Install range (for example, `10,000,000+`)
- `minInstalls` – Minimum installs
- `realInstalls` – Estimated real installs

### Pricing

- `price` – Price in currency (0 if free)
- `currency` – Currency code (for example, `USD`)
- `free` – Boolean flag signalling the app is free
- `offersIAP` – App lists in-app purchases
- `inAppProductPrice` – In-app purchase price range
- `sale` – App is currently discounted
- `originalPrice` – Original price during a sale

### Media

- `icon` – Icon URL
- `headerImage` – Header image URL
- `screenshots` – List of screenshot URLs
- `video` – Promo video URL
- `videoImage` – Video thumbnail URL

### Developer

- `developer` – Developer name
- `developerId` – Developer ID
- `developerEmail` – Contact email
- `developerWebsite` – Website URL
- `developerAddress` – Physical address
- `developerPhone` – Contact phone
- `privacyPolicy` – Privacy policy URL

### Category

- `genre` – Primary category (for example, `Communication`)
- `genreId` – Category ID (for example, `COMMUNICATION`)
- `categories` – List of categories

### Technical

- `version` – Current version
- `androidVersion` – Minimum Android version required
- `minAndroidApi` – Minimum API level
- `maxAndroidApi` – Maximum API level

### Dates

- `released` – Release date
- `lastUpdated` – Last update date
- `updatedTimestamp` – Update timestamp

### Content

- `contentRating` – Age rating (for example, `Everyone`)
- `contentRatingDescription` – Rating description
- `whatsNew` – Recent change log
- `permissions` – Permissions dictionary
- `dataSafety` – Data safety entries

### Advertising & Availability

- `adSupported` – App contains ads
- `containsAds` – Alias for `adSupported`
- `available` – App availability flag

## Search Methods

- `appId`
- `title`
- `icon`
- `url`
- `developer`
- `score`
- `scoreText`
- `currency`
- `price`
- `free`
- `summary`

## Reviews Methods

- `reviewId`
- `userName`
- `userImage`
- `score`
- `content`
- `thumbsUpCount`
- `appVersion`
- `at` (ISO 8601 timestamp)

## Developer Methods

- `appId`
- `title`
- `icon`
- `url`
- `developer`
- `description`
- `score`
- `scoreText`
- `currency`
- `price`
- `free`

## List Methods

- `appId`
- `title`
- `icon`
- `screenshots`
- `url`
- `developer`
- `genre`
- `installs`
- `score`
- `scoreText`
- `currency`
- `price`
- `free`
- `description`

## Similar Methods

- `appId`
- `title`
- `icon`
- `url`
- `developer`
- `description`
- `score`
- `scoreText`
- `currency`
- `price`
- `free`

## Suggest Methods

Returns a list of suggestion strings (no structured fields).

```python
suggestions = scraper.suggest_analyze("fitness")
# ['fitness tracker', 'fitness app', 'fitness watch', ...]
```

## List Methods: Collections

- `TOP_FREE` – Top free apps
- `TOP_PAID` – Top paid apps
- `TOP_GROSSING` – Top grossing apps

## App Categories

- `APPLICATION`
- `COMMUNICATION`
- `SOCIAL`
- `PRODUCTIVITY`
- `ENTERTAINMENT`
- `TOOLS`
- `BUSINESS`
- `FINANCE`
- `EDUCATION`
- `HEALTH_AND_FITNESS`
- `PHOTOGRAPHY`
- `MUSIC_AND_AUDIO`
- `NEWS_AND_MAGAZINES`
- `SHOPPING`
- `TRAVEL_AND_LOCAL`
- `BOOKS_AND_REFERENCE`
- `LIFESTYLE`
- `WEATHER`
- `MAPS_AND_NAVIGATION`
- `FOOD_AND_DRINK`
- `DATING`
- `BEAUTY`
- `MEDICAL`
- `SPORTS`
- `PARENTING`
- `PERSONALIZATION`
- `AUTO_AND_VEHICLES`
- `HOUSE_AND_HOME`
- `ART_AND_DESIGN`
- `EVENTS`
- `COMICS`
- `LIBRARIES_AND_DEMO`
- `VIDEO_PLAYERS`
- `WATCH_FACE`
- `ANDROID_WEAR`
- `FAMILY`

## Game Categories

- `GAME`
- `GAME_ACTION`
- `GAME_ADVENTURE`
- `GAME_ARCADE`
- `GAME_BOARD`
- `GAME_CARD`
- `GAME_CASINO`
- `GAME_CASUAL`
- `GAME_EDUCATIONAL`
- `GAME_MUSIC`
- `GAME_PUZZLE`
- `GAME_RACING`
- `GAME_ROLE_PLAYING`
- `GAME_SIMULATION`
- `GAME_SPORTS`
- `GAME_STRATEGY`
- `GAME_TRIVIA`
- `GAME_WORD`

## Reviews Sort Options

- `NEWEST` – Most recent reviews (default)
- `RELEVANT` – Most helpful reviews
- `RATING` – Sorted by rating value

```python
scraper.reviews_analyze("com.whatsapp", sort="NEWEST")
scraper.reviews_analyze("com.whatsapp", sort="RELEVANT")
scraper.reviews_analyze("com.whatsapp", sort="RATING")
```
