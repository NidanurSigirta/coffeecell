"""Application settings loaded from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Uygulama ayarları.
    Pydantic, .env dosyasındaki değerleri okuyup otomatik validate eder.
    """

    # Application
    app_name: str = "CoffeeCell"
    app_env: str = "development"
    app_debug: bool = True

    # Database
    database_url: str

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",   # .env'de fazladan değişken varsa patlatma
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """CORS origin'lerini virgülle ayrılmış string'den listeye çevir."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Singleton — tüm uygulamada tek bir settings objesi
settings = Settings()