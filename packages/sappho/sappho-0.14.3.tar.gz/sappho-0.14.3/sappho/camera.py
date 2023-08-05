"""Camera control on a surface.

Camera is just a pygame surface, so treat it as such!

A camera allows you to have a viewport which is smaller than the size
of the surface you're hoping to pan that viewport around on. Think
about looking at a big painting through a paper towel tube.

Cameras have an output resolution it scales its viewport to, plus a
behavior which governs how a Camera pans on its associated surface.

"""

import pygame


class CameraOutOfBounds(Exception):
    """The subsurface, which is the camera's view,
    goes beyond the surface the camera's viewing.

    Camera has been moved so that its area exceeds
    the surface it uses to make a subsurface.

    Attributes:
        camera (Camera):

    """

    def __init__(self, camera):
        super(CameraOutOfBounds, self).__init__(camera)
        self.camera = camera


class CameraBehavior(object):
    """How a camera moves. How it handles boundaries,
    character movement, etc.

    This CameraBehavior, the default, keeps the focal rectangle
    in the top left of the camera view.

    You'll want to inherit this class when creating
    a CameraBehavior, including overriding the
    move method.

    """

    @staticmethod
    def move(camera, focal_rectangle):
        """Move the camera, keeping the focal rectangle in
        the top left of the camera view.

        This method should be overridden in a child class.

        Arguments:
            camera (sappho.camera.Camera): Associated
                Sappho camera object to control.
            focal_rectangle (pygame.Rect): Rectangle which
                is used to possibly adjust camera position.

        """

        scroll_position = focal_rectangle.topleft
        camera.view_rect.topleft = scroll_position


class CameraCenterBehavior(CameraBehavior):
    """A camera behavior that centers the
    focal rectangle on the screen.

    Will not cause Camera.update_state() to raise
    CameraOutOfBounds, because the move logic
    prevents such from occuring!

    """

    @staticmethod
    def move(camera, focal_rectangle):
        """Move the camera, keeping the focal rectangle
        in the center of the screen where possible.

        Arguments:
            camera (sappho.camera.Camera):
            focal_rectangle (pygame.Rect): Rectangle which
                is used to possibly adjust camera position.

        """

        new_view_rect = camera.view_rect.copy()
        new_view_rect.center = focal_rectangle.center

        # Make sure the camera isn't centered in a way that
        # exceeds the environment's dimensions (don't go off
        # the map!)
        if new_view_rect.left < 0:
            new_view_rect.left = 0

        if new_view_rect.top < 0:
            new_view_rect.top = 0

        if new_view_rect.bottom > camera.source_resolution[1]:
            new_view_rect.bottom = camera.source_resolution[1]

        if new_view_rect.right > camera.source_resolution[0]:
            new_view_rect.right = camera.source_resolution[0]

        camera.view_rect = new_view_rect


class Camera(pygame.surface.Surface):
    """Surface that acts as a scrollable view, with optional scaling
    onto another surface.

    Attributes:
        source_resolution (tuple[int, int]): Maximum size of the
            environment being portrayed. If you have a map with many
            inconsistently sized layers, this should be the size of
            all of those layers flattened onto a single new layer.
            Anything beyond this size will not be on camera.
        output_resolution (tuple[int, int]): Resolution to scale up the
            view of the surface to
        view_rect (pygame.Rect): Rectangle area of this camera's view,
            which is used to create the subsurface, which is scaled
            to output_resolution and blit to self/camera.
        behavior (CameraBehavior): The initial behavior to use for this
            Camera. The :py:class:`CameraBehavior <sappho.CameraBehavior>`
            that this Camera uses to control movement.

    """

    def __init__(self, source_resolution, output_resolution,
                 view_resolution, behavior=None):

        """Create a Camera!

        Arguments:
            view_resolution (tuple[int, int]): used to create
                view_rect attribute.

        """

        super(Camera, self).__init__(output_resolution)

        self.source_surface = pygame.surface.Surface(source_resolution,
                                                     pygame.SRCALPHA)
        self.source_resolution = source_resolution
        self.output_resolution = output_resolution
        self.view_rect = pygame.Rect((0, 0), view_resolution)
        self.behavior = behavior or CameraBehavior()

    def update_state(self, timedelta):
        """Update the Camera to point to the
        current scroll position.

        Gets the "view" from the current scroll position
        and camera resolution. That view is used to create
        a subsurface of the "source subsurface," scaled to
        the target_resolution. The new subsurface is then
        blit to the camera (which is a surface, itself!).

        Arguments:
            timedelta (None): This isn't used at all, but it
                is included as an argument for consistency.

        """

        try:
            subsurface = self.source_surface.subsurface(self.view_rect)
        except ValueError:
            raise CameraOutOfBounds(self)

        scaled_surface = pygame.transform.scale(subsurface,
                                                self.output_resolution)

        # Blit the scaled surface to this camera (which is also a surface)
        super(Camera, self).blit(scaled_surface, (0, 0))

    def scroll_to(self, focal_rectangle):
        """Scroll to the given focal rectangle using the current behavior.

        Parameters:
            focal_rectangle (pygame.Rect): Rectangle to possibly update
                the view position to using the camera's current behavior

        """

        self.behavior.move(self, focal_rectangle)
