import { ApiError } from './errors.js';

export const defaultOwnerEmail = 'olutimehintobi@gmail.com';
export type RequestLimits = { perMinute: number; perDay: number };

export function createRequestBudget(
  limits: RequestLimits = { perMinute: 30, perDay: 200 },
  now: () => number = Date.now,
) {
  if (![limits.perMinute, limits.perDay].every(value => Number.isSafeInteger(value) && value > 0)) {
    throw new Error('Request limits must be positive integers.');
  }
  let minute = -1, day = -1, minuteCount = 0, dayCount = 0;
  return () => {
    const time = now();
    const currentMinute = Math.floor(time / 60_000);
    const currentDay = Math.floor(time / 86_400_000);
    if (minute !== currentMinute) { minute = currentMinute; minuteCount = 0; }
    if (day !== currentDay) { day = currentDay; dayCount = 0; }
    const resetAt = dayCount >= limits.perDay ? (day + 1) * 86_400_000
      : minuteCount >= limits.perMinute ? (minute + 1) * 60_000 : undefined;
    if (resetAt !== undefined) {
      throw new ApiError(429, 'RATE_LIMITED', 'The request limit has been reached. Try again later.',
        undefined, Math.max(1, Math.ceil((resetAt - time) / 1000)));
    }
    // shortcut: counters reset when this process restarts; use shared durable quotas before paid hosting.
    minuteCount++;
    dayCount++;
  };
}
