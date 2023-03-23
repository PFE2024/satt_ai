var mongoose_1 = __importDefault(require("mongoose"));
var mongoose_paginate_1 = __importDefault(require("mongoose-paginate"));
//2)
var twitterSchema = new mongoose_1["default"].Schema({
   
});
//3)
twitterSchema.plugin(mongoose_paginate_1["default"]);
var twitter = mongoose_1["default"].model("twitter", twitterSchema);
exports["default"] = twitter;