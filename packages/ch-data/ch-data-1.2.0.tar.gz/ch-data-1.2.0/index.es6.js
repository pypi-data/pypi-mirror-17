import find from "lodash/find";
import flatten from "lodash/flatten";
import invert from "lodash/invert";
import kebabCase from "lodash/kebabCase";
import memoize from "lodash/memoize";
import pluck from "lodash/map";
import snakeCase from "lodash/snakeCase";
import zip from "lodash/zip";

import locations from "./locations";
import manufacturers from "./manufacturers";
import models from "./trucks";
import states from "./states";

// Conditionally require jquery
let hasWindow = (typeof window !== "undefined");

if ( hasWindow ) {
  // Pre process
  document.addEventListener("DOMContentLoaded", () => {
    let
      $ = window.jQuery || window.$,
      hasCloudinary = $ && $.cloudinary;

    manufacturers.forEach( m => {
      hasCloudinary && (
        m.logo = $.cloudinary.url( m.logo, { transformation: ["model_image"]})
      );

      m.slug = snakeCase( m.name )
      m.icon = kebabCase( m.slug )
    });

    hasCloudinary && models.forEach( m => {
      if ( !!m.image )
        m.image = $.cloudinary.url( m.image, { transformation: ["model_image"]});
    });
 });

}

// Calc all available body types
let allAvailableBodyTypesSet = new Set(
    flatten( pluck( models, "available_body_types") )
  ),
  allVehicleTypesSet = new Set(
    pluck( models, "type" )
  );

export const
  getStateCode = name => invert( states )[ name ],
  getStateName = code => states[ code ],
  getOBDEnabledModels = year => models.filter( model => model.year >= 2010 ),
  isOBDEnabled = model => model.year >= 2010,

  getModel = memoize(
    model => find( models, { model })
  ),

  allAvailableBodyTypes = Array.from( allAvailableBodyTypesSet ),

  getBodyTypes = model => {
    let found = getModel( model );
    return found ? found.available_body_types : [];
  },

  allVehicleTypes = zip(
    Array.from( allVehicleTypesSet ), [

    // Order matters
    // Separate icon names
    "platform-body",
    "flat-bed-trailer",
    "tipper",
    "transit-mixer",
    "bulker",
    "tanker",
    "bus",
    "bus"

  ]).map( ([name, icon]) => {
    return {
      name,
      slug: snakeCase( name ),
      icon
    };
  });

export {
  manufacturers,
  models,
  states,
  locations
};
