export interface ResourceSnapshot<T> {
  key: string;
  data: T | null;
  loading: boolean;
  error: Error | null;
}

/** Prevent rendering the previous symbol/refresh's data or errors for a new request. */
export function visibleResource<T>(snapshot: ResourceSnapshot<T>, key: string) {
  if (snapshot.key !== key) {
    return { data: null, loading: true, error: null };
  }
  return { data: snapshot.data, loading: snapshot.loading, error: snapshot.error };
}
