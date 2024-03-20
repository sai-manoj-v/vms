// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React from "react";
import { MapView } from "@aws-amplify/ui-react-geo";
import { NavigationControl } from "react-map-gl";
import { TrackerControl } from "./components/tracking/TrackerControl";
// import { DistanceControl } from "./components/routing/DistanceControl";

const coordinates = {
  longitude: -111.6725008,
  latitude: 33.310020,
};

const App = () => {
  return (
    <MapView
      initialViewState={{
        ...coordinates,
        zoom: 15,
      }}
      style={{
        width: "100vw",
        height: "100vh",
      }}
    >
      <NavigationControl position={"top-right"} />
      <TrackerControl />
    </MapView>
  );
};

export default App;
