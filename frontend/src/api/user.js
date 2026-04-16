export function userRegister(data) {
  return request({
    url: '/api/v1/auth/register',
    method: 'post',
    data
  })
}