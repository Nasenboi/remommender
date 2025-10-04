import {type RouteConfig, index, route, prefix} from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  ...prefix("library", [
    ...prefix("albums", [
      index("routes/albums.tsx"),
      route(":albumId", "routes/album-detail.tsx")
    ])
  ])
] satisfies RouteConfig;
