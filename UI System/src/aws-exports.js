const awsconfig = {
  aws_appsync_region: "us-west-2",
  aws_appsync_authenticationType: "API_KEY",
  aws_appsync_graphqlEndpoint:
    "https://smn2m4bw7ng4pohvjmoi4ub5ae.appsync-api.us-west-2.amazonaws.com/graphql",
  aws_appsync_apiKey: "da2-u6ug7ugmjfe3znrku6szikuem4",
  Auth: {
    region: "us-west-2",
    identityPoolId: "us-west-2:c43ef702-a6d9-4676-be26-028c2be42f79",
  },
  geo: {
    AmazonLocationService: {
      maps: {
        items: {
          ["BELIV_IoT_Tracker"]: {
            style: "HERE Explore",
          },
        },
        default: "BELIV_IoT_Tracker",
      },
      region: "us-west-2",
    },
  },
};

export default awsconfig;
