describe('MobileAdPlacer', function () {
  var mobileAdPlacer = require('./mobile-ad-placer');
  var faker = require('faker');


  describe('placeAdsByWordCountByWordCount', function () {
    var article;
    var paragraph;

    beforeEach(function () {
      article = document.createElement('section');
      article.setAttribute('class', 'article-text');
      paragraph = document.createElement('p');
      document.body.appendChild(article);
      window.ads = {loadAds: function() { return }};
    });

    afterEach(function () {
      article.remove();
    });

    it('places ad after 350 words', function () {
      paragraph.innerHTML = faker.lorem.words(351);
      article.appendChild(paragraph);
      mobileAdPlacer.placeAdsByWordCount();

      var responseClassName = article.children[1].getAttribute('class');
      expect(responseClassName).to.equal("dfp dfp-slot-inread");
    });

    it('places multiple ads', function () {
      paragraph.innerHTML = faker.lorem.words(351);
      article.appendChild(paragraph);

      var secondParagraph = document.createElement('p');
      secondParagraph.innerHTML = faker.lorem.words(352);
      article.appendChild(secondParagraph);
      mobileAdPlacer.placeAdsByWordCount();

      var ads = article.getElementsByClassName('dfp-slot-inread');
      expect(ads.length).to.equal(2);
    });

    it('only places ads after paragraph breaks', function () {
      paragraph.innerHTML = faker.lorem.words(1000);
      article.appendChild(paragraph);

      mobileAdPlacer.placeAdsByWordCount();
      var adCount = article.getElementsByClassName('dfp').length;
      expect(adCount).to.equal(1); // sanity check ad is placed

      var adsInsideParagraph = paragraph.getElementsByClassName('dfp').length;
      expect(adsInsideParagraph).to.equal(0);
    });

    it('places no more than 4 ads', function () {
      for(var i = 0; i < 5; i++) {
        var p = document.createElement('p');
        p.innerHTML = faker.lorem.words(351);
        article.appendChild(p);
      }
      mobileAdPlacer.placeAdsByWordCount();

      var ads = article.getElementsByClassName('dfp');
      expect(ads.length).to.equal(4);
    });

    it('does not call loadAds() if window.ads is undefined', function () {
      window.ads = undefined;
      expect(mobileAdPlacer.placeAdsByWordCount).to.not.throw(Error);
    });
  });

  describe('placeAdsByWordCountByParagraph', function () {
    var article;
    var paragraph;

    beforeEach(function () {
      article = document.createElement('section');
      article.setAttribute('class', 'article-text');
      for (var i = 0; i < 25; i++) {
        paragraph = document.createElement('p');
        article.appendChild(paragraph);
      };
      $('body').append(article);
      window.ads = {loadAds: function() { return }};
      mobileAdPlacer.placeAdsByParagraph();
    });

    afterEach(function () {
      article.remove();
    });

    it('appends first ad after the 2nd paragraph', function () {
      var responseClass = article.childNodes[2].getAttribute('class');
      expect(responseClass).to.equal('dfp dfp-slot-inread');
    });

    it('appends second ad after the 5th paragraph', function () {
      var responseClass = article.childNodes[6].getAttribute('class');
      expect(responseClass).to.equal('dfp dfp-slot-inread');
    });

    it('appends third ad after the 9th paragraph', function () {
      var responseClass = article.childNodes[11].getAttribute('class');
      expect(responseClass).to.equal('dfp dfp-slot-inread');
    });

    it('appends fourth ad after the 14th paragraph', function () {
      var responseClass = article.childNodes[17].getAttribute('class');
      expect(responseClass).to.equal('dfp dfp-slot-inread');
    });

    it('does not append ad after the last paragraph', function () {
      article.innerHTML = '';
      article.appendChild(document.createElement('p'));
      article.appendChild(document.createElement('p'));
      mobileAdPlacer.placeAdsByParagraph();
      expect(article.children.length).to.equal(2);
    });

    it('appends no more than 4 ads', function () {
      var adDivs = article.getElementsByClassName('dfp dfp-slot-inread');
      expect(adDivs.length).to.equal(4);
    });
  });
});
