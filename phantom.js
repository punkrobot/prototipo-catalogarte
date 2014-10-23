var page = require('webpage').create();
var system = require('system');

var address = system.args[1];
var file = system.args[2];

/*page.paperSize = {
    format: 'A4',
    orientation: 'landscape'
};*/

page.open(address, function() {
  page.render(file);
  phantom.exit();
});
