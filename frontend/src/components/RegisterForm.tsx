'use client';

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

interface RegisterFormData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  confirm_password: string;
  accept_cgu: boolean;
}

interface RegisterFormErrors {
  first_name?: string;
  last_name?: string;
  email?: string;
  password?: string;
  confirm_password?: string;
  accept_cgu?: string;
  general?: string;
}

const initialFormData: RegisterFormData = {
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  confirm_password: '',
  accept_cgu: false,
};

const RegisterForm: React.FC = () => {
  const [formData, setFormData] = useState<RegisterFormData>(initialFormData);
  const [errors, setErrors] = useState<RegisterFormErrors>({});
  const [successMessage, setSuccessMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const { name, value, type, checked } = e.target;
      setFormData((prev) => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value,
      }));
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    },
    []
  );

  const validate = (data: RegisterFormData): RegisterFormErrors => {
    const newErrors: RegisterFormErrors = {};
    if (!data.first_name.trim()) newErrors.first_name = 'Le prénom est requis.';
    if (!data.last_name.trim()) newErrors.last_name = 'Le nom est requis.';
    if (!data.email.trim()) {
      newErrors.email = 'L’adresse email est requise.';
    } else if (
      !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(data.email)
    ) {
      newErrors.email = 'Adresse email invalide.';
    }
    if (!data.password) newErrors.password = 'Le mot de passe est requis.';
    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{12,}$/.test(data.password)) {
      newErrors.password = 'Mot de passe trop faible. Min 12 caractères avec majuscule, minuscule, chiffre et caractère spécial.';
    }
    if (data.password !== data.confirm_password)
      newErrors.confirm_password = 'Les mots de passe ne correspondent pas.';
    if (!data.accept_cgu)
      newErrors.accept_cgu = 'Vous devez accepter les CGU.';
    return newErrors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setSuccessMessage('');

    const validationErrors = validate(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setIsSubmitting(true);
    try {
      const payload = {
        first_name: formData.first_name.trim(),
        last_name: formData.last_name.trim(),
        email: formData.email.trim(),
        password: formData.password,
        confirm_password: formData.confirm_password,
        accept_cgu: formData.accept_cgu,
      };

      await axios.post('/api/register/', payload, {
        timeout: 10000,
        headers: { 'Content-Type': 'application/json' },
      });

      setSuccessMessage('Inscription réussie !');
      setFormData(initialFormData);

      setTimeout(() => {
        router.push('/login');
      }, 1500);
    } catch (err: unknown) {
      if (
        typeof err === 'object' &&
        err !== null &&
        'response' in err &&
        (err as { response?: { data?: RegisterFormErrors } }).response?.data
      ) {
        setErrors((err as { response: { data: RegisterFormErrors } }).response.data);
      } else {
        setErrors({ general: 'Une erreur s’est produite. Veuillez réessayer.' });
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-4 w-full max-w-md p-4 border rounded bg-white shadow"
      autoComplete="off"
      noValidate
    >
      <h2 className="text-xl font-semibold text-center">Créer un compte</h2>

      <input
        name="first_name"
        type="text"
        placeholder="Prénom"
        value={formData.first_name}
        onChange={handleChange}
        className="p-2 border rounded"
        autoComplete="given-name"
        required
        minLength={2}
        maxLength={50}
      />
      {errors.first_name && <p className="text-red-500 text-sm">{errors.first_name}</p>}

      <input
        name="last_name"
        type="text"
        placeholder="Nom"
        value={formData.last_name}
        onChange={handleChange}
        className="p-2 border rounded"
        autoComplete="family-name"
        required
        minLength={2}
        maxLength={50}
      />
      {errors.last_name && <p className="text-red-500 text-sm">{errors.last_name}</p>}

      <input
        name="email"
        type="email"
        placeholder="Adresse email"
        value={formData.email}
        onChange={handleChange}
        className="p-2 border rounded"
        autoComplete="email"
        required
        maxLength={100}
      />
      {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}

      <input
        name="password"
        type="password"
        placeholder="Mot de passe"
        value={formData.password}
        onChange={handleChange}
        className="p-2 border rounded"
        autoComplete="new-password"
        required
        minLength={8}
      />
      {errors.password && <p className="text-red-500 text-sm">{errors.password}</p>}

      <input
        name="confirm_password"
        type="password"
        placeholder="Confirmer le mot de passe"
        value={formData.confirm_password}
        onChange={handleChange}
        className="p-2 border rounded"
        autoComplete="new-password"
        required
        minLength={8}
      />
      {errors.confirm_password && (
        <p className="text-red-500 text-sm">{errors.confirm_password}</p>
      )}

      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          name="accept_cgu"
          checked={formData.accept_cgu}
          onChange={handleChange}
          required
        />
        J’accepte les conditions générales d’utilisation
      </label>
      {errors.accept_cgu && <p className="text-red-500 text-sm">{errors.accept_cgu}</p>}

      {errors.general && <p className="text-red-500 text-sm">{errors.general}</p>}
      {successMessage && <p className="text-green-600 text-sm text-center">{successMessage}</p>}

      <button
        type="submit"
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded disabled:opacity-60"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Inscription...' : 'S’inscrire'}
      </button>
    </form>
  );
};

export default RegisterForm;
