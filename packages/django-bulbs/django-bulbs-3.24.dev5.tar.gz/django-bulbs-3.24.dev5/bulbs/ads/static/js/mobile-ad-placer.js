'use strict';

var MobileAdPlacer = {
  placeAdsByWordCount: function () {
    var article = MobileAdPlacer.getArticle();
    if (!article) {
      return;
    }
    var paragraphs = MobileAdPlacer.getArticleParagraphs(article);
    var wordCount = 0;
    var adsPlaced = 0;

    // loop through paragphs array
    for (var i = 0; i < paragraphs.length; i++) {
      var paragraphInnerHtml = paragraphs[i].innerHTML;
      var paragraphLength = MobileAdPlacer.wordCount(paragraphInnerHtml);
      wordCount = wordCount + paragraphLength;

      if(wordCount > 350 && adsPlaced < 4) {
        var ad = MobileAdPlacer.adHtml();
        paragraphs[i].insertAdjacentElement('afterend', ad);
        wordCount = 0;
        adsPlaced++;
      }
    }
    MobileAdPlacer.loadAds();
  },

  placeAdsByParagraph: function () {
    var article = MobileAdPlacer.getArticle();
    if (!article) {
      return;
    }
    var paragraphs = MobileAdPlacer.getArticleParagraphs(article);
    var adsPlaced = 0;
    var paragraphsBetweenAds = 2;
    var adAfterParagraph= 2;


    // loop through paragphs array
    for (var i = 0; i < paragraphs.length; i++) {
      if (i === adAfterParagraph && adsPlaced < 4) {
        var ad = MobileAdPlacer.adHtml()
        paragraphs[i].insertAdjacentElement('afterend', ad);
        adsPlaced++;
        paragraphsBetweenAds++;
        adAfterParagraph = adAfterParagraph + paragraphsBetweenAds;
      }
    }
    MobileAdPlacer.loadAds();
  },

  wordCount: function (paragraph) {
    return paragraph.split(' ').length;
  },

  loadAds: function () {
    if (window.ads) {
      window.ads.loadAds();
    }
  },

  getArticle: function () {
    var articleText = document.getElementsByClassName('article-text')[0];
    if (articleText) {
      return articleText;
    }
    var contentText = document.getElementsByClassName('content-text')[0];
    if (contentText) {
      return contentText;
    }
    return false;
  },

  getArticleParagraphs: function (article) {
    var childNodeClass = article.children[1].getAttribute('class');
    if (childNodeClass && childNodeClass.includes('infographic')) {
      return article.getElementsByTagName('li');
    }
    return article.getElementsByTagName('p');
  },

  adHtml: function () {
    var ad = document.createElement('div')
    ad.setAttribute('class', 'dfp dfp-slot-inread');
    ad.setAttribute('data-ad-unit', 'inread');
    ad.innerHTML = 'Content continues below advertisement';
    return ad;
  },
};

module.exports = MobileAdPlacer;
