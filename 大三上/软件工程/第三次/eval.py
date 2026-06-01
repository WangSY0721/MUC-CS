# tag::train_generator_imports[]
from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.oneplane import OnePlaneEncoder
from keras.models import load_model  # <1>

# end::train_generator_imports[]

# tag::train_generator_generator[]
go_board_rows, go_board_cols = 19, 19
num_classes = go_board_rows * go_board_cols
num_games = 100

encoder = OnePlaneEncoder((go_board_rows, go_board_cols))  # <1>

processor = GoDataProcessor(encoder=encoder.name())  # <2>


def main():
    # 加载训练好的模型
    model = load_model('./models/small_model_epoch_300.h5')  # <1>

    test_generator = processor.load_go_data('test', num_games, use_generator=True)  # <2>

    batch_size = 128
    # 进行模型评估
    score = model.evaluate_generator(generator=test_generator.generate(batch_size, num_classes),  # <3>
                                     steps=test_generator.get_num_samples() / batch_size)  # <4>

    print(f"Test Loss: {score[0]}, Test Accuracy: {score[1]}")  # 打印评估结果


if __name__ == '__main__':
    main()
