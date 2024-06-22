from datetime import datetime, timezone

from bson import ObjectId
from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    COLLECTION = "flavor"

    def item(self, id, name, vcpu, ram, disc):
        now = datetime.now(timezone.utc)
        return {
            "_id": id,
            "name": name,
            "vcpu": vcpu,
            "ram": ram,
            "disc": disc,
            "created_at": now,
            "updated_at": now,
        }

    def flavor(self):
        return self.db[self.COLLECTION]

    def upgrade(self):
        self.flavor().insert_many(
            [
                self.item(ObjectId("667322e89a241357c97fcfd7"), "Pequeno", 2, 4, 100),
                self.item(ObjectId("667324c79a241357c97fcfd8"), "Médio", 4, 8, 200),
                self.item(ObjectId("667324d19a241357c97fcfd9"), "Grande", 8, 16, 300),
            ]
        )

    def downgrade(self):
        """Não faz nada"""
