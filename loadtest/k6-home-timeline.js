

import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 20,
  duration: '30s'
};

export default function () {
  const user = Math.floor(Math.random()*1000)+1;
  const res = http.get(`http://localhost:8080/timeline/home?user_id=${user}&limit=30`);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(0.2);
}
