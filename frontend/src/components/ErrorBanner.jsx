export default function ErrorBanner({ error }) {
  if (!error) return null;

  return (
    <div className="mb-6 rounded-2xl border border-amber-400/40 bg-amber-400/10 p-4 text-sm text-amber-200">
      Backend API unavailable: {error.message}. Showing mock data fallback.
    </div>
  );
}
