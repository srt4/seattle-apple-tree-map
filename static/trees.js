var DISPLAY_FIELDS = [
  "ownership",
  "currentStatus",
  "modDate",
  "plantedDate",
  "scientificName"
];

var createPopupDetails = function(tree) {
  var details = "<hr />";
  DISPLAY_FIELDS.forEach(function(field) {
    details += "<strong>" + field + ":</strong> "
      + tree[field] + " <br/>";
  });
  return details;
}

$(document).ready(function() {
  $.getJSON('/trees', function(trees) {
    trees.forEach(function(tree) {
      console.log("Adding a tree...");
      L.marker([tree.shapeLat, tree.shapeLng]).addTo(map)
        .bindPopup(
            tree.commonName
            + " @ "
            + tree.unitDesc
            + createPopupDetails(tree)
        );
      });
  });
});
