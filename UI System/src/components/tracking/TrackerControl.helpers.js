// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { Hub, API, graphqlOperation } from "aws-amplify";
import { onUpdatePosition } from "../common/subscriptions";

/**
 * Handler for position updates coming from the AppSync subscription
 */
const handlePositionUpdate = ({ value: { data } }) => {
  const { onUpdatePosition } = data;
  console.debug("Position updated", onUpdatePosition);
  const { longitude, latitude } = onUpdatePosition;
  Hub.dispatch("positionUpdates", { event: "positionUpdate", data: { longitude, latitude } });
};

/**
 * Helper function to unsubscribe from the AppSync subscriptions
 */
const unsubscribe = (subscriptionsRef) => {
  // Unsubscribe to the onUpdatePosition mutation
  subscriptionsRef.current?.positionUpdates?.unsubscribe();
  console.info("Unsubscribed from onUpdatePosition AppSync mutation");
};

/**
 * Helper function to susbscribe from the AppSync subscriptions
 */
const subscribe = (subscriptionsRef) => {
  // Subscribe to the onUpdatePosition mutation
  subscriptionsRef.current.positionUpdates = API.graphql(
    graphqlOperation(onUpdatePosition)
  ).subscribe({
    next: handlePositionUpdate,
    error: (err) => console.error(err),
  });
  console.info("Subscribed to onUpdatePosition AppSync mutation");
};

export { subscribe, unsubscribe };
