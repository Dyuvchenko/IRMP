from core.cameras.camera import Camera

camera = Camera()
camera.run()


class CamerasController:
    camera = camera

    # определяет, транслируется ли сигнал с камеры на web странице
    cam_translation = False
    pass
