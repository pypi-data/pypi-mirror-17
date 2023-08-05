import unittest2
import featureflow as ff
import numpy as np

from zounds.util import simple_in_memory_settings
from preprocess import Slicer, PreprocessingPipeline


class SlicerTests(unittest2.TestCase):
    def get_model(self, slicex):
        @simple_in_memory_settings
        class Model(ff.BaseModel):
            sliced = ff.PickleFeature(
                    Slicer,
                    slicex=slicex,
                    store=False)

            pipeline = ff.PickleFeature(
                    PreprocessingPipeline,
                    needs=(sliced,),
                    store=True)

        return Model

    def test_can_slice_array_with_slice_instance(self):
        training = np.ones((100, 30))
        Model = self.get_model(slicex=slice(10, 20))
        _id = Model.process(sliced=training)
        model = Model(_id)
        data = np.ones((100, 30))
        transformed = model.pipeline.transform(data)
        self.assertEqual((100, 10), transformed.data.shape)
        inverted = transformed.inverse_transform()
        self.assertEqual((100, 30), inverted.shape)
        np.testing.assert_allclose(transformed.data, 1)
        np.testing.assert_allclose(inverted[:, :10], 0)
        np.testing.assert_allclose(inverted[:, 20:], 0)

    def test_can_slice_multi_dimensional(self):
        training = np.ones((100, 30, 50))
        Model = self.get_model(slicex=slice(10, 20))
        _id = Model.process(sliced=training)
        model = Model(_id)
        data = np.ones((100, 30, 50))
        transformed = model.pipeline.transform(data)
        self.assertEqual((100, 30, 10), transformed.data.shape)
        inverted = transformed.inverse_transform()
        self.assertEqual((100, 30, 50), inverted.shape)
        np.testing.assert_allclose(transformed.data, 1)
        np.testing.assert_allclose(inverted[..., :10], 0)
        np.testing.assert_allclose(inverted[..., 20:], 0)