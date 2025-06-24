from aiogram import F, Router
from scenes.registration.is_museum_worker_scene import RegistrationIsMuseumWorkerScene
from scenes.registration.name_input_scene import RegistrationNameInputScene
from scenes.registration.which_museum_scene import RegistrationWhichMuseumScene
from scenes.registration.sphere_of_activity_scene import RegistrationSphereOfActivityScene


registration_scenes_router = Router()

registration_scenes_router.callback_query.register(RegistrationNameInputScene.as_handler(), F.data == "registration")


registration_scenes_registry = (
    RegistrationNameInputScene,
    RegistrationIsMuseumWorkerScene,
    RegistrationWhichMuseumScene,
    RegistrationSphereOfActivityScene
)

__all__ = [
    "registration_scenes_router",
    "registration_scenes_registry",
]
