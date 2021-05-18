# PyVirtuCamera
# Copyright (c) 2021 Pablo Javier Garcia Gonzalez.
# 
# Redistribution and use of the software module "PyVirtuCamera" (the “Software”)
# is permitted, free of charge, provided that the following conditions are met:
#     * Redistributions must reproduce the above copyright notice,
#       this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * You may not decompile, disassemble, reverse engineer or modify
#       any portion of the Software.
# 
# THE SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from abc import ABCMeta, abstractmethod

__all__ = ("VCBase",)


class VCBase(metaclass=ABCMeta):
    """ Abstract base class that must be overloaded to implement most
    of its methods, where each method is dedicated to set or get some
    specific data related to the scene, the cameras, viewport capturing,
    server feedback, and custom script calling.

    Methods in this class will be called asyncronously from
    virtucamera.VCServer as needed.

    All methods will always receive the instance of virtucamera.VCServer
    that is calling them as the second argument 'vcserver'.
    This can be used to access the server API as needed.
    """


    # SCENE STATE RELATED METHODS:
    # ---------------------------

    @abstractmethod
    def get_playback_state(self, vcserver):
        """ Must Return the playback state of the scene as a tuple or list
        in the following order: (current_frame, range_start, range_end)
        * current_frame (float) - The current frame number.
        * range_start (float) - Animation range start frame number.
        * range_end (float) - Animation range end frame number.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.

        Returns
        -------
        tuple or list of 3 floats
            playback state as (current_frame, range_start, range_end)
        """

        pass

    @abstractmethod
    def get_playback_fps(self, vcserver):
        """ Must return a float value with the scene playback rate
        in Frames Per Second.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.

        Returns
        -------
        float
            scene playback rate in FPS.
        """

        pass

    @abstractmethod
    def set_frame(self, vcserver, frame):
        """ Must set the current frame number on the scene

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        frame : float
            The current frame number.
        """

        pass

    @abstractmethod
    def set_playback_range(self, vcserver, start, end):
        """ Must set the animation frame range on the scene

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        start : float
            Animation range start frame number.
        end : float
            Animation range end frame number.
        """

        pass
        
    @abstractmethod
    def start_playback(self, vcserver, forward):
        """ This method must start the playback of animation in the scene.
        Not used at the moment, but must be implemented just in case
        the app starts using it in the future. At the moment
        VCBase.set_frame() is called instead.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        forward : bool
            if True, play the animation forward, if False, play it backwards.
        """

        pass

    @abstractmethod
    def stop_playback(self, vcserver):
        """ This method must stop the playback of animation in the scene.
        Not used at the moment, but must be implemented just in case
        the app starts using it in the future.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        """

        pass


    # CAMERA RELATED METHODS:
    # -----------------------

    @abstractmethod
    def get_scene_cameras(self, vcserver):
        """ Must Return a list or tuple with the names of all the scene cameras.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.

        Returns
        -------
        tuple or list
            names of all the scene cameras.
        """

        pass

    @abstractmethod
    def get_camera_exists(self, vcserver, camera_name):
        """ Must Return True if the specified camera exists in the scene,
        False otherwise.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to check for.

        Returns
        -------
        bool
            'True' if the camera 'camera_name' exists, 'False' otherwise.
        """

        pass

    @abstractmethod
    def get_camera_has_keys(self, vcserver, camera_name):
        """ Must Return whether the specified camera has animation keyframes
        in the transform or flocal length parameters, as a tuple or list,
        in the following order: (transform_has_keys, focal_length_has_keys)
        * transform_has_keys (bool) - True if the transform has keyframes.
        * focal_length_has_keys (bool) - True if the flen has keyframes.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to check for.

        Returns
        -------
        tuple or list of 2 bool
            whether the camera 'camera_name' has keys or not as
            (transform_has_keys, focal_length_has_keys)
        """

        pass

    @abstractmethod
    def get_camera_focal_length(self, vcserver, camera_name):
        """ Must Return the focal length value of the specified camera.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to get the data from.

        Returns
        -------
        float
            focal length value of the camera 'camera_name'.
        """

        pass

    @abstractmethod
    def get_camera_transform(self, vcserver, camera_name):
        """ Must return a tuple or list of 16 floats with the 4x4
        transform matrix of the specified camera.

        * The up axis must be Y+
        * The order must be:
            (rxx, rxy, rxz, 0,
            ryx, ryy, ryz, 0,
            rzx, rzy, rzz, 0,
            tx,  ty,  tz,  1)
            Being 'r' rotation and 't' translation,

        Is your responsability to rotate or transpose the matrix if needed,
        most 3D softwares offer fast APIs to do so.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to get the data from.

        Returns
        -------
        tuple or list of 16 float
            4x4 transform matrix as
            (rxx, rxy, rxz, 0, ryx, ryy, ryz, 0, rzx, rzy, rzz, 0 , tx, ty, tz, 1)
        """

        pass

    @abstractmethod
    def set_camera_focal_length(self, vcserver, camera_name, focal_length):
        """ Must set the focal length of the specified camera.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to set the focal length to.
        focal_length : float
            focal length value to be set on the camera 'camera_name'
        """

        pass

    @abstractmethod
    def set_camera_transform(self, vcserver, camera_name, transform_matrix):
        """  Must set the transform of the specified camera.
        The transform matrix is provided as a tuple of 16 floats
        with a 4x4 transform matrix.

        * The up axis is Y+
        * The order is:
            (rxx, rxy, rxz, 0,
            ryx, ryy, ryz, 0,
            rzx, rzy, rzz, 0,
            tx,  ty,  tz,  1)
            Being 'r' rotation and 't' translation,

        Is your responsability to rotate or transpose the matrix if needed,
        most 3D softwares offer fast APIs to do so.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to set the transform to.
        transform_matrix : tuple of 16 floats
            transformation matrix to be set on the camera 'camera_name'
        """

        pass

    @abstractmethod
    def set_camera_flen_keys(self, vcserver, camera_name, keyframes, focal_length_values):
        """ Must set keyframes on the focal length of the specified camera.
        The frame numbers are provided as a tuple of floats and
        the focal length values are provided as a tuple of floats
        with a focal length value for every keyframe.

        The first element of the 'keyframes' tuple corresponds to the first
        element of the 'focal_length_values' tuple, the second to the second,
        and so on.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to set the keyframes to.
        keyframes : tuple of floats
            Frame numbers to create the keyframes on.
        focal_length_values : tuple of floats
            focal length values to be set as keyframes on the camera 'camera_name'
        """

        pass

    @abstractmethod
    def set_camera_transform_keys(self, vcserver, camera_name, keyframes, transform_matrix_values):
        """ Must set keyframes on the transform of the specified camera.
        The frame numbers are provided as a tuple of floats and
        the transform matrixes are provided as a tuple of tuples of 16 floats
        with 4x4 transform matrixes, with a matrix for every keyframe.

        The first element of the 'keyframes' tuple corresponds to the first
        element of the 'transform_matrix_values' tuple, the second to the second,
        and so on.

        * The up axis is Y+
        * The order is:
            (rxx, rxy, rxz, 0,
            ryx, ryy, ryz, 0,
            rzx, rzy, rzz, 0,
            tx,  ty,  tz,  1)
            Being 'r' rotation and 't' translation,

        Is your responsability to rotate or transpose the matrixes if needed,
        most 3D softwares offer fast APIs to do so.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to set the keyframes to.
        keyframes : tuple of floats
            Frame numbers to create the keyframes on.
        transform_matrix_values : tuple of tuples of 16 floats
            transformation matrixes to be set as keyframes on the camera 'camera_name'
        """

        pass

    @abstractmethod
    def remove_camera_keys(self, vcserver, camera_name):
        """ This method must remove all transform
        and focal length keyframes in the specified camera.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to remove the keyframes from.
        """

        pass

    @abstractmethod
    def create_new_camera(self, vcserver):
        """ This method must create a new camera in the scene
        and return its name.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.

        Returns
        -------
        str
            Newly created camera name.
        """

        pass


    # VIEWPORT CAPTURE RELATED METHODS:
    # ---------------------------------

    @abstractmethod
    def capture_will_start(self, vcserver):
        """ This method is called whenever a client app requests a video
        feed from the viewport. Usefull to init a pixel buffer
        or other objects you may need to capture the viewport

        IMPORTANT! Calling vcserver.set_capture_resolution() and
        vcserver.set_capture_mode() here is a must. Please check
        the documentation for those methods.

        You can also call vcserver.set_vertical_flip() here optionally,
        if you need to flip your pixel buffer. Disabled by default.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        """

        pass

    def capture_did_end(self, vcserver):
        """ Optional, this method is called whenever a client app
        stops the viewport video feed. Usefull to destroy a pixel buffer
        or other objects you may have created to capture the viewport.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        """

        pass

    def get_capture_coords(self, vcserver, camera_name):
        """ If vcserver.capture_mode == vcserver.CAPMODE_SCREENSHOT, it must
        return a tuple or list with the left-top coordinates (x,y)
        of the screen region to be captured, being 'x' the horizontal axis
        and 'y' the vertical axis. If you don't use CAPMODE_SCREENSHOT,
        you don't need to overload this method.

        If the screen region has changed in size from the previous call to
        this method, and therefore the capture resolution is different,
        vcserver.set_capture_resolution() must be called here before returning.
        You can use vcserver.capture_width and vcserver.capture_height
        to check the previous resolution.

        The name of the camera selected in the app is provided,
        as can be usefull to set-up the viewport render in some cases.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera that is currently selected in the App.

        Returns
        -------
        tuple or list of 2 float
            left-top screen coordinates of the capture region as (x,y).
        """

        pass

    def get_capture_buffer(self, vcserver, camera_name):
        """ If vcserver.capture_mode == vcserver.CAPMODE_BUFFER, it must
        return a contiguous buffer as a Python bytes-like object
        implementing the 'Buffer Protocol', containing raw pixels of
        the viewport image. If you don't use CAPMODE_BUFFER,
        you don't need to overload this method.

        If the capture resolution has changed in size from the previous call to
        this method, vcserver.set_capture_resolution() must be called here
        before returning. You can use vcserver.capture_width and
        vcserver.capture_height to check the previous resolution.

        The name of the camera selected in the app is provided,
        as can be usefull to set-up the viewport render in some cases.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera that is currently selected in the App.

        Returns
        -------
        object - Buffer protocol
            raw pixels of the viewport image as a contiguous Python buffer
        """

        pass

    def get_capture_pointer(self, vcserver, camera_name):
        """ If vcserver.capture_mode == vcserver.CAPMODE_BUFFER_POINTER,
        it must return an int representing a memory address to the first
        element of a contiguous buffer containing raw pixels of the 
        viewport image. The buffer must be kept allocated untill the next
        call to this function, is your responsability to do so.
        If you don't use CAPMODE_BUFFER_POINTER
        you don't need to overload this method.

        If the capture resolution has changed in size from the previous call to
        this method, vcserver.set_capture_resolution() must be called here
        before returning. You can use vcserver.capture_width and
        vcserver.capture_height to check the previous resolution.

        The name of the camera selected in the app is provided,
        as can be usefull to set-up the viewport render in some cases.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera that is currently selected in the App.

        Returns
        -------
        int
            value of the memory address to the first element of the buffer.
        """

        pass

    @abstractmethod
    def look_through_camera(self, vcserver, camera_name):
        """ This method must set the viewport to look through
        the specified camera.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        camera_name : str
            Name of the camera to look through
        """

        pass


    # APP/SERVER FEEDBACK METHODS:
    # ----------------------------

    def client_connected(self, vcserver, client_ip, client_port):
        """ Optional, this method is called whenever a client app
        connects to the server. Usefull to give the user
        feedback about a successfull connection.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        client_ip : str
            ip address of the remote client
        client_port : int
            port number of the remote client
        """

        pass

    def client_disconnected(self, vcserver):
        """ Optional, this method is called whenever a client app
        disconnects from the server, even if it's disconnected by calling
        stop_serving() with the virtucamera.VCServer API. Usefull to give
        the user feedback about the disconnection.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        """

        pass

    def current_camera_changed(self, vcserver, current_camera):
        """ Optional, this method is called when the user selects
        a different camera from the app. Usefull to give the user
        feedback about the currently selected camera.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        current_camera : str
            Name of the new selected camera
        """
        
        pass

    def server_did_stop(self, vcserver):
        """ Optional, calling stop_serving() on virtucamera.VCServer
        doesn't instantly stop the server, it is done in the background
        due to the asyncronous nature of some of its processes.
        This method is called when all services have been completely
        stopped.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        """

        pass


    # CUSTOM SCRIPT METHODS:
    # ----------------------

    def get_script_labels(self, vcserver):
        """ Optionally Return a list or tuple of str with the labels of
        custom scripts to be called from VirtuCamera App. Each label is
        a string that identifies the script that will be showed
        as a button in the App.

        The order of the labels is important. Later if the App asks
        to execute a script, an index based on this order will be provided
        to VCBase.execute_script(), so that method must also be implemented.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.

        Returns
        -------
        tuple or list of str
            custom script labels.
        """

        pass

    def execute_script(self, vcserver, script_index, current_camera):
        """ Only required if VCBase.get_script_labels()
        has been implemented. This method is called whenever the user
        taps on a custom script button in the app.
        
        Each of the labels returned from VCBase.get_script_labels()
        identify a custom script that is showed as a button in the app.
        The order of the labels is important and 'script_index' is a 0-based
        index representing what script to execute from that list/tuple.

        This function must return True if the script executed correctly,
        False if there where errors. It's recommended to print any errors,
        so that the user has some feedback about what went wrong.

        You may want to provide a way for the user to refer to the currently
        selected camera in their scripts, so that they can act over it.
        'current_camera' is provided for this situation.

        Parameters
        ----------
        vcserver : virtucamera.VCServer object
            Instance of virtucamera.VCServer calling this method.
        script_index : int
            Script number to be executed.
        current_camera : str
            Name of the currently selected camera
        """

        return False