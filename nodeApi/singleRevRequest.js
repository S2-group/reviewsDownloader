var gplay = require('google-play-scraper');


function extractReviewId(reviewUrl){
  if (typeof reviewUrl != 'undefined') {
    return reviewUrl.slice(-119);
  }
}

var appId = process.argv[2].trim();
var page =  process.argv[3];
var input = {
              appId: appId,
              page: page,
              sort: gplay.sort.RATING
            };

gplay.reviews(input).then(function(apps){
  apps.forEach(function(app){
    console.log(JSON.stringify(app))
  });
  process.exit()
}).catch(function(e){
  console.log('There was an error fetching the reviews!');
  console.log(e.message);
  process.exit(1)
});
