const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
        let response;

        if (isSignUp) {
            // Validation for required fields
            if (formData.password !== formData.confirm_password) {
                setError('Passwords do not match');
                setIsLoading(false);
                return;
            }

            if (!formData.email || !formData.password) {
                setError('Email and Password are required');
                setIsLoading(false);
                return;
            }

            response = await axios.post('http://127.0.0.1:8000/api/auth/register/', {
                email: formData.email,
                username: formData.username || formData.email,
                password: formData.password,
            });
        } else {
            // Login
            if (!formData.email || !formData.password) {
                setError('Email and Password are required');
                setIsLoading(false);
                return;
            }

            response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
                email: formData.email,
                password: formData.password
            });
        }

        // Ensure response contains the token and user
        if (response.data.token && response.data.user) {
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user', JSON.stringify(response.data.user));

            // Redirect based on signup or login
            navigate(isSignUp ? '/userinfo' : '/home');
        } else {
            setError('Invalid response from server');
        }
    } catch (err) {
        console.error('Auth error:', err);
        let errorMessage = 'An error occurred';

        if (err.response?.data) {
            // Enhanced error handling
            if (typeof err.response.data === 'string') {
                errorMessage = err.response.data;
            } else if (err.response.data.error) {
                errorMessage = err.response.data.error;
            } else if (err.response.data.detail) {
                errorMessage = err.response.data.detail;
            } else if (err.response.data.non_field_errors) {
                errorMessage = err.response.data.non_field_errors[0];
            } else {
                errorMessage = 'Unknown error';
            }
        }

        setError(errorMessage);
    } finally {
        setIsLoading(false);
    }
};
