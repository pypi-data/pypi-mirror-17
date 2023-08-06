from image import *
from ip import *


# TODO add intrinsic parameters
# TODO add remove lens distortion


class Intrinsic:
    """
    BoofCV Intrinsic Camera parameters
    """
    def __init__(self):
        # Intrinsic calibration matrix
        self.fx=0
        self.fy=0
        self.skew=0
        self.cx = 0
        self.cy = 0
        # image shape
        self.width = 0
        self.height = 0
        # radial distortion
        self.radial = None
        # tangential terms
        self.t1 = 0
        self.t2 = 0

    def load_xml(self, file_name):
        file_path = os.path.abspath(file_name)
        boof_intrinsic = gateway.jvm.boofcv.io.UtilIO.loadXML(file_path)

        if boof_intrinsic is None:
            raise RuntimeError("Can't load intrinsic parameters")

        self.set_from_boof(boof_intrinsic)

    def set_matrix(self, fx, fy, skew, cx, cy):
        self.fx = fx
        self.fy = fy
        self.skew = skew
        self.cx = cx
        self.cy = cy

    def set_image(self, width, height):
        self.width = width
        self.height = height

    def set_distortion(self, radial=None,t1=0,t2=0):
        self.radial = radial
        self.t1 = t1
        self.t2 = t2

    def set(self, orig):
        self.fx = orig.fx
        self.fy = orig.fy
        self.skew = orig.skew
        self.cx = orig.cx
        self.cy = orig.cy
        self.width = orig.width
        self.height = orig.height
        self.radial = orig.radial
        self.t1 = orig.t1
        self.t2 = orig.t2

    def set_from_boof(self, boof_intrinsic):
        self.fx = boof_intrinsic.getFx()
        self.fy = boof_intrinsic.getFy()
        self.cx = boof_intrinsic.getCx()
        self.cy = boof_intrinsic.getCy()
        self.skew = boof_intrinsic.getSkew()
        self.width = boof_intrinsic.getWidth()
        self.height = boof_intrinsic.getHeight()
        self.radial = boof_intrinsic.getRadial()
        self.t1 = boof_intrinsic.getT1()
        self.t2 = boof_intrinsic.getT2()

    def convert_to_boof(self):
        boof_intrinsic = gateway.jvm.boofcv.struct.calib.IntrinsicParameters()
        boof_intrinsic.setFx(self.fx)
        boof_intrinsic.setFy(self.fy)
        boof_intrinsic.setCx(self.cx)
        boof_intrinsic.setCy(self.cy)
        boof_intrinsic.setSkew(self.skew)
        boof_intrinsic.setWidth(self.width)
        boof_intrinsic.setHeight(self.height)
        boof_intrinsic.setRadial(self.radial)
        boof_intrinsic.setT1(self.t1)
        boof_intrinsic.setT2(self.t2)
        return boof_intrinsic

    def is_distorted(self):
        return (self.radial is not None) or self.t1 != 0 or self.t2 != 0

    def __str__(self):
        out = "Intrinsic{{ fx={:f} fy={:f} skew={:f} cx={:f} cy={:f} | width={:d} height={:d} ".\
            format(self.fx,self.fy,self.skew,self.cx,self.cy,self.width,self.height)
        if self.is_distorted():
            out += " | radial="+str(self.radial)+" t1="+str(self.t1)+" t1="+str(self.t2)+" }"
        else:
            out += "}}"
        return out


class AdjustmentType:
    NONE=0
    FULL_VIEW=1
    EXPAND=2


def adjustment_to_java( value ):
    if value == AdjustmentType.NONE:
        return gateway.jvm.boofcv.alg.distort.AdjustmentType.valueOf("NONE")
    elif value == AdjustmentType.FULL_VIEW:
        return gateway.jvm.boofcv.alg.distort.AdjustmentType.valueOf("FULL_VIEW")
    elif value == AdjustmentType.EXPAND:
        return gateway.jvm.boofcv.alg.distort.AdjustmentType.valueOf("EXPAND")
    else:
        raise RuntimeError("Unknown type")

def remove_distortion( input, output, intrinsic, adjustment=AdjustmentType.FULL_VIEW, border=Border.ZERO):
    image_type = ImageType(input.getImageType())
    distorter, java_intrinsic_out = create_remove_lens_distortion(intrinsic,image_type,adjustment,border)
    distorter.apply(input,output)
    intrinsic_out = Intrinsic()
    intrinsic_out.set_from_boof(java_intrinsic_out)
    return intrinsic_out

def create_remove_lens_distortion( intrinsic, image_type, adjustment=AdjustmentType.FULL_VIEW, border=Border.ZERO ):
    java_image_type = image_type.get_java_object()
    java_adjustment = adjustment_to_java(adjustment)
    java_border = border_to_java(border)
    java_intrinsic = intrinsic.convert_to_boof()
    java_intrinsic_out = gateway.jvm.boofcv.struct.calib.IntrinsicParameters()
    id =  gateway.jvm.boofcv.alg.distort.LensDistortionOps.imageRemoveDistortion(java_adjustment,java_border,java_intrinsic,java_intrinsic_out,java_image_type)
    return [ImageDistort(id),java_intrinsic_out]