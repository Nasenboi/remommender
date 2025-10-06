import {type RouteConfig, index, route, prefix} from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  ...prefix("library", [
    ...prefix("albums", [
      index("routes/albums.tsx"),
      route(":albumId", "routes/album-detail.tsx")
    ]),
    ...prefix("songs", [
      route("add", "routes/add-song.tsx")
    ])
  ])
] satisfies RouteConfig;
