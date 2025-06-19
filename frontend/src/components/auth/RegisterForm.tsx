'use client';

import React, { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { API_ROUTES } from '@/lib/apiRoutes';
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

const getPasswordStrength = (password: string) => {
  const length = password.length;
  const hasLower = /[a-z]/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasDigit = /\d/.test(password);
  const hasSpecial = /[^a-zA-Z\d]/.test(password);
  const score = [hasLower, hasUpper, hasDigit, hasSpecial].filter(Boolean).length;

  if (length < 8) return { level: 'Faible', color: 'bg-red-500', width: 'w-1/4' };
  if (length < 12 || score < 4) return { level: 'Moyen', color: 'bg-yellow-500', width: 'w-2/4' };
  return { level: 'Fort', color: 'bg-green-600', width: 'w-full' };
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
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(data.email)) {
      newErrors.email = 'Adresse email invalide.';
    }
    if (!data.password) {
      newErrors.password = 'Le mot de passe est requis.';
    } else if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d]).{12,}$/.test(data.password)) {
      newErrors.password =
        'Mot de passe trop faible. Min 12 caractères avec majuscule, minuscule, chiffre et caractère spécial.';
    }
    if (data.password !== data.confirm_password) {
      newErrors.confirm_password = 'Les mots de passe ne correspondent pas.';
    }
    if (!data.accept_cgu) {
      newErrors.accept_cgu = 'Vous devez accepter les CGU.';
    }
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

      await axios.post(API_ROUTES.REGISTER, payload);

      setSuccessMessage('Inscription réussie !');
      setFormData(initialFormData);

      setTimeout(() => {
        router.push('/login');
      }, 1500);
    } 
      catch (err: unknown) {
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

  const passwordStrength = getPasswordStrength(formData.password || '');

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-4 w-full max-w-md p-4 border rounded bg-white shadow"
      autoComplete="off"
      noValidate
    >
      <h2 className="text-xl font-semibold text-center">Créer un compte</h2>

      <input name="first_name" type="text" placeholder="Prénom" value={formData.first_name} onChange={handleChange} className="p-2 border rounded" required />
      {errors.first_name && <p className="text-red-500 text-sm">{errors.first_name}</p>}

      <input name="last_name" type="text" placeholder="Nom" value={formData.last_name} onChange={handleChange} className="p-2 border rounded" required />
      {errors.last_name && <p className="text-red-500 text-sm">{errors.last_name}</p>}

      <input name="email" type="email" placeholder="Adresse email" value={formData.email} onChange={handleChange} className="p-2 border rounded" required />
      {errors.email && <p className="text-red-500 text-sm">{errors.email}</p>}

      <input name="password" type="password" placeholder="Mot de passe" value={formData.password || ''} onChange={handleChange} className="p-2 border rounded" required />
      {errors.password && <p className="text-red-500 text-sm">{errors.password}</p>}

      {formData.password && (
        <div className="flex flex-col gap-1">
          <div className="w-full h-2 bg-gray-200 rounded overflow-hidden">
            <div className={`${passwordStrength.color} ${passwordStrength.width} h-full transition-all duration-300`} />
          </div>
          <p className="text-sm">Sécurité : <strong>{passwordStrength.level}</strong></p>
        </div>
      )}

      <input name="confirm_password" type="password" placeholder="Confirmer le mot de passe" value={formData.confirm_password || ''} onChange={handleChange} className="p-2 border rounded" required />
      {errors.confirm_password && <p className="text-red-500 text-sm">{errors.confirm_password}</p>}

      <label className="flex items-center gap-2 text-sm">
        <input type="checkbox" name="accept_cgu" checked={formData.accept_cgu} onChange={handleChange} required />
        J’accepte les conditions générales d’utilisation
      </label>
      {errors.accept_cgu && <p className="text-red-500 text-sm">{errors.accept_cgu}</p>}

      {errors.general && <p className="text-red-500 text-sm">{errors.general}</p>}
      {successMessage && <p className="text-green-600 text-sm text-center">{successMessage}</p>}

      <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded disabled:opacity-60" disabled={isSubmitting}>
        {isSubmitting ? 'Inscription...' : 'S’inscrire'}
      </button>
    </form>
  );
};

export default RegisterForm;
