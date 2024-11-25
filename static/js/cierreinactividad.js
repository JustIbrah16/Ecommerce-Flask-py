const idleTimeLimit = 3600000; 
    let idleTimer;

    
    function resetIdleTimer() {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(showSessionTimeoutAlert, idleTimeLimit);
    }

    
    function showSessionTimeoutAlert() {
        Swal.fire({
            icon: 'warning',
            title: '¡Tu sesión ha expirado!',
            text: 'Por favor, vuelve a iniciar sesión.',
            confirmButtonText: 'Cerrar sesión',
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '/logout'; 
            }
        });
    }

    //Eventos de actividad del usuario (movimiento del mouse, pulsaciones de teclas)
    window.onload = resetIdleTimer; 
    window.onmousemove = resetIdleTimer;
    window.onkeydown = resetIdleTimer;