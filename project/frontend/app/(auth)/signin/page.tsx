/**
 * Sign In page
 *
 * Allows existing users to authenticate and access their tasks.
 */

import { Metadata } from 'next';
import Link from 'next/link';
import { AuthForm } from '@/components/AuthForm';
import { Card, CardBody, CardHeader } from '@/components/ui/Card';

export const metadata: Metadata = {
  title: 'Sign In - Todo Evolution',
  description: 'Sign in to your Todo Evolution account',
};

export default function SignInPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 px-4 py-12">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block mb-4">
            <h1 className="text-3xl font-bold text-gray-900">Todo Evolution</h1>
          </Link>
          <p className="text-gray-600">Sign in to manage your tasks</p>
        </div>

        {/* Sign In Form Card */}
        <Card variant="elevated">
          <CardHeader>
            <h2 className="text-2xl font-semibold text-gray-900">Sign In</h2>
          </CardHeader>
          <CardBody>
            <AuthForm mode="signin" />
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
      </div>
    </div>
  );
}
