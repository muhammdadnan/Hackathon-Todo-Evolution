import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <main className="max-w-4xl mx-auto px-4 py-16 text-center">
        {/* Hero Section */}
        <div className="mb-12">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
            Todo Evolution
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-2">
            Phase 2: Full-Stack Web Application
          </p>
          <p className="text-lg text-gray-500">
            A modern todo app built with Next.js 16+ and FastAPI
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="text-3xl mb-3">🔐</div>
            <h3 className="text-lg font-semibold mb-2">Secure Authentication</h3>
            <p className="text-gray-600 text-sm">
              JWT-based authentication with user isolation
            </p>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="text-3xl mb-3">⚡</div>
            <h3 className="text-lg font-semibold mb-2">Modern Stack</h3>
            <p className="text-gray-600 text-sm">
              Next.js App Router, TypeScript, Tailwind CSS
            </p>
          </div>
          <div className="bg-white rounded-lg p-6 shadow-md">
            <div className="text-3xl mb-3">🚀</div>
            <h3 className="text-lg font-semibold mb-2">Type-Safe API</h3>
            <p className="text-gray-600 text-sm">
              FastAPI backend with SQLModel ORM
            </p>
          </div>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Link
            href="/signin"
            className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-md"
          >
            Sign In
          </Link>
          <Link
            href="/signup"
            className="px-8 py-3 bg-white text-blue-600 rounded-lg font-medium hover:bg-gray-50 transition-colors shadow-md border border-blue-600"
          >
            Sign Up
          </Link>
        </div>

        {/* Status Notice */}
        <div className="mt-12 bg-yellow-50 border border-yellow-200 rounded-lg p-4 max-w-2xl mx-auto">
          <p className="text-sm text-yellow-800">
            <strong>Development Status:</strong> Foundation phase complete. User authentication and task management features are being implemented.
          </p>
        </div>

        {/* Tech Stack */}
        <div className="mt-12 text-sm text-gray-500">
          <p className="mb-2">Built with Spec-Driven Development</p>
          <div className="flex flex-wrap justify-center gap-3">
            <span className="px-3 py-1 bg-white rounded-full text-xs">Next.js 16+</span>
            <span className="px-3 py-1 bg-white rounded-full text-xs">FastAPI</span>
            <span className="px-3 py-1 bg-white rounded-full text-xs">PostgreSQL</span>
            <span className="px-3 py-1 bg-white rounded-full text-xs">TypeScript</span>
            <span className="px-3 py-1 bg-white rounded-full text-xs">Tailwind CSS</span>
          </div>
        </div>
      </main>
    </div>
  );
}
