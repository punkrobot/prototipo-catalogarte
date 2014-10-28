var page = require('webpage').create();
var system = require('system');

var address = system.args[1];
var file = system.args[2];

page.paperSize = {
    width: '730px',
    height: '600px',
    border: '0px'
};

page.open(address, function () {
    page.render(file);
    phantom.exit();
});
