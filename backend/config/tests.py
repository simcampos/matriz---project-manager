from django.test import SimpleTestCase

from config.database import database_config


class DatabaseConfigTests(SimpleTestCase):
    def test_database_url_is_used_when_configured(self):
        config = database_config(
            {
                "DATABASE_URL": (
                    "postgresql://app%40user:p%40ss@db.example.com:5433/matriz%20prod"
                    "?sslmode=require"
                ),
                "POSTGRES_DB": "ignored",
            }
        )

        self.assertEqual(config["NAME"], "matriz prod")
        self.assertEqual(config["USER"], "app@user")
        self.assertEqual(config["PASSWORD"], "p@ss")
        self.assertEqual(config["HOST"], "db.example.com")
        self.assertEqual(config["PORT"], "5433")
        self.assertEqual(config["OPTIONS"], {"sslmode": "require"})

    def test_postgres_variables_remain_supported_without_database_url(self):
        config = database_config(
            {
                "POSTGRES_DB": "matriz",
                "POSTGRES_USER": "matriz_user",
                "POSTGRES_PASSWORD": "local-password",
                "POSTGRES_HOST": "db",
                "POSTGRES_PORT": "5432",
            }
        )

        self.assertEqual(config["NAME"], "matriz")
        self.assertEqual(config["USER"], "matriz_user")
        self.assertEqual(config["HOST"], "db")
        self.assertEqual(config["PORT"], "5432")

    def test_invalid_database_url_fails_explicitly(self):
        with self.assertRaisesRegex(ValueError, "valid PostgreSQL connection URL"):
            database_config({"DATABASE_URL": "https://example.com/not-a-database"})
