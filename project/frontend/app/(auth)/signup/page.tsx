/**
 * Sign Up page
 *
 * Allows new users to create an account and start using the app.
 */

import { Metadata } from 'next';
import Link from 'next/link';
import { AuthForm } from '@/components/AuthForm';
import { Card, CardBody, CardHeader } from '@/components/ui/Card';

export const metadata: Metadata = {
  title: 'Sign Up - Todo Evolution',
  description: 'Create your Todo Evolution account',
};

export default function SignUpPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4 py-12">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block mb-4">
            <h1 className="text-3xl font-bold text-gray-900">Todo Evolution</h1>
          </Link>
          <p className="text-gray-600">Create your account to get started</p>
        </div>

        {/* Sign Up Form Card */}
        <Card variant="elevated">
          <CardHeader>
            <h2 className="text-2xl font-semibold text-gray-900">Sign Up</h2>
          </CardHeader>
          <CardBody>
            <AuthForm mode="signup" />
          </CardBody>
        </Card>

        {/* Back to home link */}
        <div className="text-center mt-6">
          <Link
            href="/"
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            ← Back to home
          </Link>
        </div>

        {/* Terms notice */}
        <p className="text-xs text-gray-500 text-center mt-4">
          By signing up, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}
