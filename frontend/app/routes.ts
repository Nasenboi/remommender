import {type RouteConfig, index, route} from "@react-router/dev/routes";

export default [
    index("routes/home.tsx"),
    route("library/albums", "routes/albums.tsx")
] satisfies RouteConfig;
