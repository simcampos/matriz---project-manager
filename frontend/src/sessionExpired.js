export function shouldDispatchSessionExpiredEvent(path, status) {
  return status === 401 && path !== "/sessions/" && path !== "/users/me/";
}
