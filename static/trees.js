$(document).ready(function() {
  // this formats an array into something more readable/printable.
  // example input: [209192,36,8626,TRE-41480,TRE,1225 9TH AV W,PRIV,,]
  // example output:
  //  209192
  //  36
  //  8626
  //  TRE-41480
  //  ...
  function formatArray(arr) {
    var result = '';
    arr.forEach(function(element) {
      if (element != '' && element != null) {
        result += element + '\n';
      }
    });
    return result;
  }

  $.getJSON('/trees', function(trees) {
    trees.forEach(function(tree) {
      console.log("Adding a tree...");
      L.marker([tree.latitude, tree.longitude]).addTo(map)
      	.bindPopup(tree.commonName + " @ " + tree.address + "<br />"
          + "<pre>" + formatArray(tree.verboseDetails) + "</pre>");
      });
  });
});
