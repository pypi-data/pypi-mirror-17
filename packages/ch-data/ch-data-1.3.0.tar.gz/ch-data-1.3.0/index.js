"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.locations = exports.states = exports.models = exports.manufacturers = exports.allVehicleTypes = exports.getBodyTypes = exports.allAvailableBodyTypes = exports.getModel = exports.isOBDEnabled = exports.getOBDEnabledModels = exports.getStateName = exports.getStateCode = undefined;

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _find = require("lodash/find");

var _find2 = _interopRequireDefault(_find);

var _flatten = require("lodash/flatten");

var _flatten2 = _interopRequireDefault(_flatten);

var _invert = require("lodash/invert");

var _invert2 = _interopRequireDefault(_invert);

var _kebabCase = require("lodash/kebabCase");

var _kebabCase2 = _interopRequireDefault(_kebabCase);

var _memoize = require("lodash/memoize");

var _memoize2 = _interopRequireDefault(_memoize);

var _map = require("lodash/map");

var _map2 = _interopRequireDefault(_map);

var _snakeCase = require("lodash/snakeCase");

var _snakeCase2 = _interopRequireDefault(_snakeCase);

var _zip = require("lodash/zip");

var _zip2 = _interopRequireDefault(_zip);

var _locations = require("./locations");

var _locations2 = _interopRequireDefault(_locations);

var _manufacturers = require("./manufacturers");

var _manufacturers2 = _interopRequireDefault(_manufacturers);

var _trucks = require("./trucks");

var _trucks2 = _interopRequireDefault(_trucks);

var _states = require("./states");

var _states2 = _interopRequireDefault(_states);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// Conditionally require jquery
var hasWindow = typeof window !== "undefined";

// Pre process
_manufacturers2.default.forEach(function (m) {
  m.slug = (0, _snakeCase2.default)(m.name);
  m.icon = (0, _kebabCase2.default)(m.slug);
});

document.addEventListener("DOMContentLoaded", function () {
  var $ = hasWindow && window.jQuery || window.$,
      hasCloudinary = $ && $.cloudinary;

  if (!hasCloudinary) return;

  _manufacturers2.default.forEach(function (m) {
    if (m.logo) m.logo = $.cloudinary.url(m.logo, { transformation: ["model_image"] });
  });

  hasCloudinary && _trucks2.default.forEach(function (m) {
    if (m.image) m.image = $.cloudinary.url(m.image, { transformation: ["model_image"] });
  });
});

// Calc all available body types
var allAvailableBodyTypesSet = new Set((0, _flatten2.default)((0, _map2.default)(_trucks2.default, "available_body_types"))),
    allVehicleTypesSet = new Set((0, _map2.default)(_trucks2.default, "type"));

var getStateCode = exports.getStateCode = function getStateCode(name) {
  return (0, _invert2.default)(_states2.default)[name];
},
    getStateName = exports.getStateName = function getStateName(code) {
  return _states2.default[code];
},
    getOBDEnabledModels = exports.getOBDEnabledModels = function getOBDEnabledModels(year) {
  return _trucks2.default.filter(function (model) {
    return model.year >= 2010;
  });
},
    isOBDEnabled = exports.isOBDEnabled = function isOBDEnabled(model) {
  return model.year >= 2010;
},
    getModel = exports.getModel = (0, _memoize2.default)(function (model) {
  return (0, _find2.default)(_trucks2.default, { model: model });
}),
    allAvailableBodyTypes = exports.allAvailableBodyTypes = Array.from(allAvailableBodyTypesSet),
    getBodyTypes = exports.getBodyTypes = function getBodyTypes(model) {
  var found = getModel(model);
  return found ? found.available_body_types : [];
},
    allVehicleTypes = exports.allVehicleTypes = (0, _zip2.default)(Array.from(allVehicleTypesSet), [

// Order matters
// Separate icon names
"platform-body", "flat-bed-trailer", "tipper", "transit-mixer", "bulker", "tanker", "bus", "bus"]).map(function (_ref) {
  var _ref2 = _slicedToArray(_ref, 2);

  var name = _ref2[0];
  var icon = _ref2[1];

  return {
    name: name,
    slug: (0, _snakeCase2.default)(name),
    icon: icon
  };
});

exports.manufacturers = _manufacturers2.default;
exports.models = _trucks2.default;
exports.states = _states2.default;
exports.locations = _locations2.default;

