export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
    public readonly details?: { field: string; message: string }[],
    public readonly retryAfter?: number,
  ) {
    super(message);
  }
}

export function preconditionFailed(): never {
  throw new ApiError(412, 'PRECONDITION_FAILED', 'The saved book changed. Fetch its current version before retrying.');
}
