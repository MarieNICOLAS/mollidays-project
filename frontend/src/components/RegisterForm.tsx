'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirmPassword: '',
    acceptCGU: false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [successMessage, setSuccessMessage] = useState('');
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrors({});
    setSuccessMessage('');

    if (formData.password !== formData.confirmPassword) {
      setErrors({ confirmPassword: 'Les mots de passe ne correspondent pas.' });
      return;
    }

    if (!formData.acceptCGU) {
      setErrors({ acceptCGU: 'Vous devez accepter les CGU.' });
      return;
    }

    try {
      const payload = {
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirmPassword,
        accept_cgu: formData.acceptCGU,
      };

      await axios.post('http://localhost:8000/api/register/', payload);

      setSuccessMessage('Inscription réussie !');
      setFormData({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirmPassword: '',
        acceptCGU: false,
      });

      setTimeout(() => {
        router.push('/login');
      }, 1500);
    } catch (error: unknown) {
      interface AxiosError {
        response?: {
          data?: Record<string, string>;
        };
      }

      if (
        typeof error === 'object' &&
        error !== null &&
        'response' in error &&
        (error as AxiosError).response?.data
      ) {
        setErrors((error as AxiosError).response!.data!);
      } else {
        setErrors({ general: 'Une erreur s’est produite. Veuillez réessayer.' });
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-md p-4 border rounded bg-white shadow">
      <h2 className="text-xl font-semibold text-center">Créer un compte</h2>

      <input
        name="first_name"
        type="text"
        placeholder="Prénom"
        value={formData.first_name}
        onChange={handleChange}
        className="p-2 border rounded"
      />
      {errors.first_name && <p className="text-red-500 text-sm">{errors.first_name}</p>}

      <input
        name="last_name"
        type="text"
        placeholder="Nom"
        value={formData.last_name}
        onChange={handleChange}
        className="p-2 border rounded"
      />
      {errors.last_name && <p className="text-red-500 text-sm">{errors.last_name}</p>}

      <input
        name="email"
        type="email"
        placeholder="Adresse email"
        value={formData.email}
        onChange={handleChange}
        className="p-2 border rounded"
      />
      {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}

      <input
        name="password"
        type="password"
        placeholder="Mot de passe"
        value={formData.password}
        onChange={handleChange}
        className="p-2 border rounded"
      />
      {errors.password && <p className="text-red-500 text-sm">{errors.password}</p>}

      <input
        name="confirmPassword"
        type="password"
        placeholder="Confirmer le mot de passe"
        value={formData.confirmPassword}
        onChange={handleChange}
        className="p-2 border rounded"
      />
      {errors.confirmPassword && <p className="text-red-500 text-sm">{errors.confirmPassword}</p>}

      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          name="acceptCGU"
          checked={formData.acceptCGU}
          onChange={handleChange}
        />
        J’accepte les conditions générales d’utilisation
      </label>
      {errors.acceptCGU && <p className="text-red-500 text-sm">{errors.acceptCGU}</p>}

      {errors.general && <p className="text-red-500 text-sm">{errors.general}</p>}
      {successMessage && <p className="text-green-600 text-sm text-center">{successMessage}</p>}

      <button
        type="submit"
        className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded"
      >
        S’inscrire
      </button>
    </form>
  );
};

export default RegisterForm;
