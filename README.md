# CSCI-2910-NewsAPI-App
A console app that allows users to save their favorite news sources or scientific pages, and perform searches through various sources.

## 2/26/25 - What Needs Work
### Domain editing function:
- Smoother process to verify valid domains
- Ability to add domains and verify before adding to database
- Set up while loops

### Feed:
- Needs to be completely set up, which includes:
- Collect all domains user set to "include",
- Search by /top-headlines,
- limit page size to 25,
- searching by most recent(publishedAt), and
- limit display to 5 articles at a time.

### Search:
- Touched, but still mostly needs to be set up, including:
- ~~Ask for keyword,~~
- ~~ask to search by either included domains, excluded domains, or an open search (ONLY IF KEYWORD IS GIVEN),~~
- ~~to sort by publish date, relevancy, or popularity,~~
- (IF TIME PERMITS) option to sort by country and language
- ~~if user is searching by /top-headline, then convert domains (abc.com) to sources (abc)~~
- if domains or source lists are empty, the string used to search by domains should be made to be empty and users should be told this.

### Etc:
- Look into ways of saving a user's endpoint between program visits (for now, set endpoint to /everything upon startup)

### Additions: 
- all known source ids and urls are now saved as two variables (

------------------------------------------------------------------------------------------------------------------------

## 2/24/25 - What Needs Work
### Domain editing function:
- Smoother process to verify valid domains
- Ability to add domains and verify before adding to database
- Set up while loops

### Feed:
- Needs to be completely set up, which includes:
- Collect all domains user set to "include",
- Search by /top-headlines,
- limit page size to 25,
- searching by most recent(publishedAt), and
- limit display to 5 articles at a time.

### Search:
- Touched, but still mostly needs to be set up, including:
- Ask for keyword,
- ask to search by either included domains, excluded domains, or an open search (ONLY IF KEYWORD IS GIVEN),
- to sort by publish date, relevancy, or popularity,
- (IF TIME PERMITS) option to sort by country and language
- if user is searching by /top-headline, then convert domains (abc.com) to sources (abc)

### Etc:
- Look into ways of saving a user's endpoint between program visits (for now, set endpoint to /everything upon startup)
