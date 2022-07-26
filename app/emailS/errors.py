class EmailVerificationError(Exception):
    def __init__(self, email, message = "unable to send email"):
        super().__init__(message)
        self.email = email
    
    def __str__(self):
        return f"{self.message} for {self.email}"
