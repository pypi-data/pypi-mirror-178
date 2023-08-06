# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
from ..technology import primitive as prm


class PrimitiveDispatcher:
    """Dispatch to class method based on type of `_Primitive` subclasses.

    This dispatcher follows the common way of working in the `dispatch` module.
    """
    def __call__(self, prim: prm._Primitive, *args, **kwargs):
        classname = prim.__class__.__name__.split(".")[-1]
        return getattr(self, classname, self._pd_unhandled)(prim, *args, **kwargs)

    def _pd_unhandled(self, prim, *args, **kwargs):
        raise RuntimeError(
            "Internal error: unhandled dispatcher for object of type "
            f"{prim.__class__.__name__}"
        )

    def _Primitive(self, prim: prm._Primitive, *args, **kwargs):
        raise NotImplementedError(
            f"No dispatcher implemented for object of type {prim.__class__.__name__}"
        )

    def _MaskPrimitive(self, prim: prm._MaskPrimitive, *args, **kwargs):
        return self._Primitive(prim, *args, **kwargs)

    def _DesignMaskPrimitive(self,
        prim: prm._DesignMaskPrimitive, *args, **kwargs,
    ):
        return self._MaskPrimitive(prim, *args, **kwargs)

    def Marker(self, prim: prm.Marker, *args, **kwargs):
        return self._DesignMaskPrimitive(prim, *args, **kwargs)

    def Auxiliary(self, prim: prm.Auxiliary, *args, **kwargs):
        return self._DesignMaskPrimitive(prim, *args, **kwargs)
    
    def _WidthSpacePrimitive(self, prim: prm._WidthSpacePrimitive, *args, **kwargs):
        if isinstance(prim, prm._DesignMaskPrimitive):
            return self._DesignMaskPrimitive(prim, *args, **kwargs)
        else:
            return self._MaskPrimitive(prim, *args, **kwargs)

    def ExtraProcess(self, prim: prm.ExtraProcess, *args, **kwargs):
        return self._WidthSpacePrimitive(prim, *args, **kwargs)

    def Implant(self, prim: prm.Implant, *args, **kwargs):
        return self._WidthSpacePrimitive(prim, *args, **kwargs)

    def Insulator(self, prim: prm.Insulator, *args, **kwargs):
        return self._WidthSpacePrimitive(prim, *args, **kwargs)

    def _Conductor(self,
        prim: prm._Conductor, *args, **kwargs,
    ):
        return self._DesignMaskPrimitive(prim, *args, **kwargs)

    def _WidthSpaceConductor(self,
        prim: prm._WidthSpaceConductor, *args, **kwargs,
    ):
        return self._WidthSpacePrimitive(prim, *args, **kwargs)

    def Well(self, prim: prm.Well, *args, **kwargs):
        # TODO: What to do with Implant superclass ?
        return self._WidthSpaceConductor(prim, *args, **kwargs)

    def DeepWell(self, prim: prm.DeepWell, *args, **kwargs):
        # TODO: What to do with Implant superclass ?
        return self._WidthSpaceConductor(prim, *args, **kwargs)

    def WaferWire(self, prim: prm.WaferWire, *args, **kwargs):
        return self._WidthSpaceConductor(prim, *args, **kwargs)

    def GateWire(self, prim: prm.GateWire, *args, **kwargs):
        return self._WidthSpaceConductor(prim, *args, **kwargs)

    def MetalWire(self, prim: prm.MetalWire, *args, **kwargs):
        return self._WidthSpaceConductor(prim, *args, **kwargs)

    def TopMetalWire(self, prim: prm.TopMetalWire, *args, **kwargs):
        return self.MetalWire(prim, *args, **kwargs)

    def MIMTop(self, prim: prm.MIMTop, *args, **kwargs):
        return self.MetalWire(prim, *args, **kwargs)

    def Via(self, prim, *args: prm.Via, **kwargs):
        return self._Conductor(prim, *args, **kwargs)

    def PadOpening(self, prim: prm.PadOpening, *args, **kwargs):
        return self._WidthSpaceConductor(prim, *args, **kwargs)

    def Resistor(self, prim: prm.Resistor, *args, **kwargs):
        return self._WidthSpacePrimitive(prim, *args, **kwargs)

    def MIMCapacitor(self, prim: prm.MIMCapacitor, *args, **kwargs):
        return self._WidthSpacePrimitive(prim, *args, **kwargs)

    def Diode(self, prim: prm.Diode, *args, **kwargs):
        return self._WidthSpacePrimitive(prim, *args, **kwargs)

    def MOSFETGate(self, prim: prm.MOSFETGate, *args, **kwargs):
        return self._WidthSpacePrimitive(prim, *args, **kwargs)

    def MOSFET(self, prim: prm.MOSFET, *args, **kwargs):
        return self._Primitive(prim, *args, **kwargs)

    def Bipolar(self, prim: prm.Bipolar, *args, **kwargs):
        return self._Primitive(prim, *args, **kwargs)

    def Spacing(self, prim: prm.Spacing, *args, **kwargs):
        return self._Primitive(prim, *args, **kwargs)
